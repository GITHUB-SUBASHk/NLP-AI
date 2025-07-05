from fastapi import APIRouter, Depends, HTTPException
from interfaces.api_server.auth import get_current_user
from interfaces.api_server.session import redis_client

router = APIRouter(prefix="/analytics", tags=["analytics"])

def require_admin(user=Depends(get_current_user)):
    if isinstance(user, dict) and user.get("role") == "admin":
        return user
    raise HTTPException(status_code=403, detail="Admin access only")

@router.get("/stats")
async def analytics_stats(user=Depends(require_admin)):
    fallback_counts = redis_client.hgetall("analytics:fallback_counts") or {}
    intent_counts = redis_client.hgetall("analytics:intent_counts") or {}
    session_count = redis_client.get("analytics:session_count") or 0

    fallback_counts = {k.decode(): int(v) for k, v in fallback_counts.items()}
    intent_counts = {k.decode(): int(v) for k, v in intent_counts.items()}
    session_count = int(session_count) if session_count else 0

    total = sum(fallback_counts.values())
    fallback_percent = {k: (v / total * 100 if total else 0) for k, v in fallback_counts.items()}
    top_intents = sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "fallback_percent": fallback_percent,
        "top_intents": top_intents,
        "session_count": session_count
    }

@router.get("/plugins")
async def analytics_plugins(user=Depends(require_admin)):
    plugin_usage = redis_client.hgetall("analytics:plugin_usage") or {}
    plugin_usage = {k.decode(): int(v) for k, v in plugin_usage.items()}
    top_plugins = sorted(plugin_usage.items(), key=lambda x: x[1], reverse=True)
    return {"plugin_usage": top_plugins}

@router.get("/weak-intents")
async def analytics_weak_intents(user=Depends(require_admin)):
    fallback_counts = redis_client.hgetall("analytics:fallback_counts") or {}
    intent_counts = redis_client.hgetall("analytics:intent_counts") or {}

    fallback_counts = {k.decode(): int(v) for k, v in fallback_counts.items()}
    intent_counts = {k.decode(): int(v) for k, v in intent_counts.items()}

    weak_intents = []
    for intent, fallback in fallback_counts.items():
        total = intent_counts.get(intent, 0)
        percent = (fallback / total * 100) if total else 0
        weak_intents.append((intent, percent, fallback, total))

    weak_intents = sorted(weak_intents, key=lambda x: x[1], reverse=True)[:5]
    return {"weak_intents": weak_intents}