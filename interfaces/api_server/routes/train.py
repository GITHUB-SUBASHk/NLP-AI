# interfaces/api_server/routes/train.py

from fastapi import APIRouter, Depends, HTTPException, status
from interfaces.api_server.auth import get_current_user
from ai.rasa.train_model import train_rasa_model

router = APIRouter(prefix="/train", tags=["rasa"])

@router.post("/")
async def trigger_training(current_user: str = Depends(get_current_user)):
    """
    Triggers RASA model training and returns the latest model name or error.
    Only available to authenticated users.
    """
    success, result = train_rasa_model()
    if success:
        return {"status": "success", "model": result}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Training failed: {result}"
        )