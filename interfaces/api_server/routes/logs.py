# interfaces/api_server/routes/logs.py
from fastapi import APIRouter, HTTPException
from interfaces.api_server.session import redis_client

router = APIRouter()

@router.get("/logs/{user_id}")
async def get_user_logs(user_id: str):
    logs = redis_client.lrange(f"logs:{user_id}", 0, 49)
    return [json.loads(log) for log in logs]