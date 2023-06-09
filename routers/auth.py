from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token





auth_router = APIRouter()

class User(BaseModel):
    email: str
    password: str


@auth_router.post('/login', tags = ['Auth'], response_model = dict, status_code = 200)
def auth(user: User) -> dict:
    token = create_token(user.dict())
    return JSONResponse(status_code = 200, content={ "token": token})
