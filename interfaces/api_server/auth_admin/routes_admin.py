from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from .auth import create_access_token, verify_token

router = APIRouter(prefix="/api/admin", tags=["admin"])

class AdminLogin(BaseModel):
    username: str
    password: str

@router.post("/token")
async def login_admin(admin: AdminLogin):
    if admin.username == "admin" and admin.password == "admin123":
        token = create_access_token({"sub": admin.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/protected")
async def protected_route(current_user: str = Depends(verify_token)):
    return {"message": f"Welcome, {current_user}!"}