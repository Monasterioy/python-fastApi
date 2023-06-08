from fastapi import FastAPI, Depends, Path, Query, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.security import HTTPBearer
from jwt_manager import create_token, validate_token
import requests 
import json
app = FastAPI(
    title="FastAPI CURSO JOSE MONASTERIO",
    description="A template for FastAPI",
    version="0.1.0",
)

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

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] ==  '':
            raise HTTPException(status_code=403, detail="Credenciales no son invalidas")


class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Mi pelicula", min_length=5, max_length=12, )
    category: str = Field(default="accion", min_length=5, max_length=12, )
    rating: float 
    description: str  
    overview: str = Field(default="Descripcion de la pelicula", min_length=5, max_length=12, )
    director: str  
    year: int = Field(default=2023, le = 2022, )  
    
class MovieToUPdate(BaseModel):
    title: str 
    category: str 
    rating: float 
    description: str  
    overview: str
    director: str  
    year: int

response_model_msg = {
    "message": "message of accion success"
}    

    
movies = [
    {
        "id": 1,
        "title": 'The Shawshank Redemption',
        "category": 'accion',
        "overview": 'That excelent movie',
        "director": 'Frank Darabont',
        "year": 1994,
        "rating": 9.2,
    },
    {
        "id": 2,
        "title": 'The Shawshank Redemption 2',
        "category": 'terror',
        "overview": 'That excelent movie',
        "director": 'Frank Darabont',
        "year": 1994,
        "rating": 9.2,
    }
]

@app.get('/movies', 
        tags=[tasgs['MOVIES']], response_model = List[Movie], status_code = 200, dependencies=[Depends(JWTBearer())])
def get_Movies() -> List[Movie]:
    return JSONResponse(content= movies)

@app.get('/movies/{id}', 
        tags = [tasgs['MOVIES']], response_model = Movie, status_code = 200)
def get_Movie(id: int = Path(le=1, ge=2000)) -> Movie:
    typeKey = 'id'
    response = filter_movies(movies, typeKey, id,)
    return JSONResponse(status_code = 200, content = response)

@app.get('/movies/', 
        tags=[tasgs['MOVIES']], response_model = List[Movie], status_code = 200 )
def get_movies_by_query(category: str = Query(max_length=15, min_length=5)) -> List[Movie]:
    typeKey = 'category'
    response = filter_movies(movies, typeKey, category)
    return JSONResponse(status_code = 200, content = response)

@app.post('/movies/', tags = [tasgs['MOVIES']], response_model = dict, status_code = 201)
def create_movie(
    movie: Movie
) -> dict:
    movies.append(movie)
    return JSONResponse( status_code = 201, content={ "message": "se registro la pelicula"})


@app.put('/movies/', tags = [tasgs['MOVIES']], response_model = dict, status_code = 200)
def update_movie(id: int, movie: Movie) -> dict:
    for  item in movies:
        if item['id'] == id:
            item['id'] = id
            item["title"] = movie.title
            item["category"] = movie.category
            item["overview"] = movie.overview
            item["director"] = movie.director
            item["year"] = movie.year
            item["rating"] = movie.rating 
            return JSONResponse(status_code = 200, content={ "message": "se actualizo la pelicula"})
        
@app.delete('/movies/', tags = [tasgs['MOVIES']], response_model = dict, status_code = 200)
def delete_movie(id: int) -> dict:
    for  item in movies:
        if item['id'] == id:
            movies.remove(item)
    return JSONResponse(status_code = 200, content={ "message": "se registro elimino la pelicula"})

@app.post('/login', tags = [tasgs['Auth']], response_model = dict, status_code = 200)
def auth(user: User) -> dict:
    token = create_token(user.dict())
    return JSONResponse(status_code = 200, content={ "token": token})


def filter_movies(movies,typeKey, key):
    return [ movie for movie in movies if movie[typeKey] == key]


