# interfaces/api_server/routes/debug.py

from fastapi import APIRouter, Depends, HTTPException, status
from interfaces.api_server.auth import get_current_user
import os, json, yaml, glob, subprocess
from typing import List, Dict, Any
from datetime import datetime, timedelta

router = APIRouter(prefix="/debug", tags=["debug"])

# --- Redis Safe Import ---
try:
    from interfaces.api_server.session import redis_client
    USE_REDIS = True
except ImportError:
    redis_client = None
    USE_REDIS = False

# --- Role-based Admin Check ---
def require_admin(user: str = Depends(get_current_user)) -> str:
    if isinstance(user, dict):
        if user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
    elif user != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

# --- 1. User Logs ---
@router.get("/logs/{user_id}")
async def get_user_logs(user_id: str, _: str = Depends(require_admin)) -> List[Dict[str, Any]]:
    if not USE_REDIS or not redis_client:
        raise HTTPException(status_code=500, detail="Redis not available")
    logs = redis_client.lrange(f"logs:{user_id}", 0, 49)
    return [json.loads(log) for log in logs]

# --- 2. Fallback Logs ---
@router.get("/fallbacks")
async def get_fallbacks(_: str = Depends(require_admin)) -> List[Dict[str, Any]]:
    if not USE_REDIS or not redis_client:
        raise HTTPException(status_code=500, detail="Redis not available")
    keys = redis_client.keys("fallbacks:*")
    all_fallbacks = []
    for key in keys:
        user_id = key.decode().split(":")[1]
        entries = redis_client.lrange(key, 0, 49)
        for entry in entries:
            log = json.loads(entry)
            log["user_id"] = user_id
            all_fallbacks.append(log)
    all_fallbacks.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return all_fallbacks

# --- 3. Stats Dashboard ---
@router.get("/stats")
async def get_stats(_: str = Depends(require_admin)) -> Dict[str, Any]:
    if not USE_REDIS or not redis_client:
        raise HTTPException(status_code=500, detail="Redis not available")
    
    session_keys = redis_client.keys("user:*:context")
    active_sessions = len(session_keys)

    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)
    fallback_count = 0
    total_count = 0
    top_intents = {}

    for key in redis_client.keys("logs:*"):
        logs = redis_client.lrange(key, 0, 49)
        for log in logs:
            entry = json.loads(log)
            ts = entry.get("timestamp")
            if ts:
                try:
                    ts_dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
                except Exception:
                    continue
                if ts_dt > one_hour_ago:
                    total_count += 1
                    if entry.get("event") == "fallback":
                        fallback_count += 1
                    intent = entry.get("intent")
                    if intent:
                        top_intents[intent] = top_intents.get(intent, 0) + 1

    fallback_pct = (fallback_count / total_count * 100) if total_count else 0
    top_intents_sorted = sorted(top_intents.items(), key=lambda x: x[1], reverse=True)

    return {
        "active_sessions": active_sessions,
        "fallback_pct_last_hour": round(fallback_pct, 2),
        "top_intents": top_intents_sorted[:5]
    }

# --- 4. Rasa Train Trigger ---
@router.post("/train")
async def trigger_rasa_train(_: str = Depends(require_admin)) -> Dict[str, Any]:
    rasa_path = os.path.abspath("rasa_core")
    if not os.path.exists(rasa_path):
        raise HTTPException(status_code=500, detail="Rasa core directory not found.")

    try:
        result = subprocess.run(
            ["rasa", "train"],
            cwd=rasa_path,
            capture_output=True,
            text=True,
            timeout=300
        )
        return {
            "status": "success" if result.returncode == 0 else "error",
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

# --- 5. View YAML Files ---
@router.get("/yaml/{type}")
async def get_yaml(type: str, _: str = Depends(require_admin)) -> Dict[str, Any]:
    file_map = {
        "nlu": "rasa_core/nlu.yml",
        "domain": "rasa_core/domain.yml",
        "stories": "rasa_core/stories.yml"
    }
    if type not in file_map:
        raise HTTPException(status_code=400, detail="Invalid type. Choose from: nlu, domain, stories")
    path = file_map[type]
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="YAML file not found")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# --- 6. Get All Intents and Responses from domain.yml ---
@router.get("/intents")
async def get_intents_and_responses(_: str = Depends(require_admin)):
    domain_path = "rasa_core/domain.yml"

    if not os.path.exists(domain_path):
        raise HTTPException(status_code=404, detail="domain.yml not found")

    try:
        with open(domain_path, "r", encoding="utf-8") as f:
            domain_data = yaml.safe_load(f)

        intents = domain_data.get("intents", [])
        responses = domain_data.get("responses", {})  # Optional: Sometimes called "utterances"

        # Normalize if needed (some Rasa versions use 'utter_' prefix, or 'utterances' key)
        return {
            "intents": intents,
            "responses": responses
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse domain.yml: {str(e)}")

# --- 7. Get Session Context ---
@router.get("/session/{user_id}")
async def get_session(user_id: str, _: str = Depends(require_admin)) -> Dict[str, str]:
    if not USE_REDIS or not redis_client:
        raise HTTPException(status_code=500, detail="Redis not available")

    context = redis_client.hgetall(f"user:{user_id}:context")
    context = {k.decode(): v.decode() for k, v in context.items()}

    if not context:
        raise HTTPException(status_code=404, detail="Session not found")

    return context