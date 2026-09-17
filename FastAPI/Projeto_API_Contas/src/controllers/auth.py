from fastapi import APIRouter, Response, status
from schemas.auth import LoginIn
from views.auth import LoginOut
from security import sign_jwt

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model = LoginOut)
async def login(data:LoginIn):
    print ("LoginIn:",data)
    return sign_jwt(user_id=data.user_id)