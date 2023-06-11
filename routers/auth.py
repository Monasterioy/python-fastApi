from fastapi import APIRouter
from fastapi.responses import JSONResponse
from jwt_manager import create_token
from schema.auth import User
auth_router = APIRouter()

@auth_router.post("/login", tags=["Auth"], response_model=dict, status_code=200)
def auth(user: User) -> dict:
    token = create_token(user.dict())
    return JSONResponse(status_code=200, content={"token": token})
