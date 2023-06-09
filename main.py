from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token, validate_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.auth import auth_router 

app = FastAPI(
    title="FastAPI CURSO JOSE MONASTERIO",
    description="A template for FastAPI",
    version="0.1.0",
)

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)

tasgs ={
    "HOME": 'Home',
    'MOVIES': 'Movies',
    "Auth": 'Auth',
}

class Config:
    schema_extra = {
        "example": {
            "id": 1,
            "title": "Mi película",
            "overview": "Descripción de la película",
            "year": 2022,
            "rating": 9.8,
            "category" : "Acción"
        }
    }