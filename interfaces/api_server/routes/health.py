# interfaces/api_server/routes/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health():
    """
    Health check endpoint for container/service monitoring.
    """
    return {"status": "ok"}