# File: interfaces/api_server/routes/admin.py

from fastapi import APIRouter, Depends, HTTPException, status
from interfaces.api_server.auth import get_current_user

# Try to import redis client (async)
try:
    from interfaces.api_server.session import redis_client as redis
    USE_REDIS = True
except ImportError:
    redis = None
    USE_REDIS = False

# In-memory fallback for user preferences
user_preferences = {}

def set_assist_enabled(user_id: str, enabled: bool):
    if USE_REDIS and redis:
        redis.set(f"user:{user_id}:assist_enabled", int(enabled))
    else:
        user_preferences[user_id] = enabled

def is_assist_enabled(user_id: str) -> bool:
    if USE_REDIS and redis:
        val = redis.get(f"user:{user_id}:assist_enabled")
        if val is not None:
            return bool(int(val))
        return True  # Default enabled
    return user_preferences.get(user_id, True)

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/user/{user_id}/toggle-assist")
async def toggle_assist(user_id: str, enabled: bool, current_user: str = Depends(get_current_user)):
    """
    Enable or disable assistant mode for a user.
    """
    set_assist_enabled(user_id, enabled)
    return {"user_id": user_id, "assist_enabled": enabled}

@router.get("/user/{user_id}/toggle-assist")
async def get_toggle_assist(user_id: str, current_user: str = Depends(get_current_user)):
    """
    Get current assistant mode status for a user.
    """
    status_ = is_assist_enabled(user_id)
    return {"user_id": user_id, "assist_enabled": status_}

@router.get("/fallback-source/{user_id}")
async def get_fallback_source(user_id: str):
    """
    Get the last fallback source (RASA, RAG, LLM, LOCAL) used for a specific user.
    """
    if USE_REDIS and redis:
        source = await redis.get(f"fallback:{user_id}")
        if source is None:
            source = "NONE"
        elif isinstance(source, bytes):
            source = source.decode()
    else:
        source = "NONE"
    return {"source": source}