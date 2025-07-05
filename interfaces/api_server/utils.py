# interfaces/api_server/utils.py

import json
import time
from typing import Any, Dict, Optional
import yaml

def utc_now_iso() -> str:
    """Return current UTC time in ISO 8601 format."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def safe_decode(val):
    """Decode Redis bytes to str if needed."""
    if isinstance(val, bytes):
        return val.decode()
    return val

def capped_redis_list(redis_client, key: str, entry: Dict[str, Any], cap: int = 50):
    """
    Push a log entry to a Redis list and trim it to a maximum length.
    """
    redis_client.lpush(key, json.dumps(entry))
    redis_client.ltrim(key, 0, cap - 1)

def parse_yaml_file(path: str) -> Optional[Dict]:
    """
    Load a YAML file and return its contents as a dictionary.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return None

def get_sender_id_from_jwt(user) -> str:
    """
    Extract sender_id from JWT payload or fallback to 'anonymous'.
    """
    if isinstance(user, dict):
        return user.get("sub") or user.get("username") or "anonymous"
    return user or "anonymous"

def is_admin(user) -> bool:
    """
    Check if the user has admin role.
    """
    if isinstance(user, dict):
        return user.get("role") == "admin"
    return False

# --- Fallback Source Logger ---

"""
Logs which engine (PLUGIN, RASA, RAG, LLM, LOCAL) handled the response for each user.
Stored per-user in Redis for admin review, or printed in dev mode.
"""

try:
    from interfaces.api_server.session import redis_client
    USE_REDIS = True
except ImportError:
    redis_client = None
    USE_REDIS = False

def log_fallback_source(user_id: str, source: str):
    """
    Logs fallback source (PLUGIN, RASA, RAG, LLM, LOCAL) to Redis or prints in dev mode.
    """
    if USE_REDIS and redis_client:
        try:
            redis_client.set(f"fallback:{user_id}", source)
        except Exception as e:
            print(f"[Fallback Log][REDIS ERROR] {user_id} → {source} ({e})")
    else:
        print(f"[Fallback Log] {user_id} → {source}")