from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from jwt_manager import create_token, validate_token
from config.database import Session
from models.movie import Movie as movieModel
from middlewares.jwt_bearer import JWTBearer

movie_router = APIRouter()

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Mi pelicula", min_length=5, max_length=12, )
    category: str = Field(default="accion", min_length=5, max_length=12, )
    rating: float 
    overview: str = Field(default="Descripcion de la pelicula", min_length=5, max_length=12, )
    year: int = Field(default=2023, le = 2040) 


tasgs ={
    'MOVIES': 'Movies',
}

@movie_router.get('/movies', 
        tags=[tasgs['MOVIES']], response_model = List[Movie], status_code = 200, dependencies=[Depends(JWTBearer())])
def get_Movies() -> List[Movie]:
    db = Session()
    all_movies = db.query(movieModel).all()
    return JSONResponse(content= jsonable_encoder(all_movies))

@movie_router.get('/movies/{id}', 
        tags = [tasgs['MOVIES']], response_model = Movie, status_code = 200)

def get_Movie(id: int = Path(le=2000, ge=0)) -> Movie:
    db = Session()
    movie_find = db.query(movieModel).filter(movieModel.id == id).first()
    if not movie_find: 
        return JSONResponse(status_code = 404, content = {"message": "Movie not found"})
    return JSONResponse(status_code = 200, content = jsonable_encoder(movie_find))

@movie_router.get('/movies/', 
        tags=[tasgs['MOVIES']], response_model = List[Movie], status_code = 200 )
def get_movies_by_query(category: str = Query(max_length=15, min_length=5)) -> List[Movie]:
    db = Session()
    movies = db.query(movieModel).filter(movieModel.category == category).all()
    return JSONResponse(status_code = 200, content = movies)

@movie_router.post('/movies/', tags = [tasgs['MOVIES']], response_model = dict, status_code = 201)
def create_movie(
    movie: Movie
) -> dict:
    db = Session()
    new_movie = movieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse( status_code = 201, content={ "message": "se registro la pelicula"})


@movie_router.put('/movies/', tags = [tasgs['MOVIES']], response_model = dict, status_code = 200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    movie_find = db.query(movieModel).filter(movieModel.id == id).first()
    if not movie_find:
        return JSONResponse(status_code=404, content= {"message": "Movie not found"})
    movie_find.title = movie.title
    movie_find.category = movie.category
    movie_find.overview = movie.overview
    movie_find.year = movie.year
    movie_find.rating = movie.rating
    db.commit()
    return JSONResponse(status_code = 200, content={ "message": "se actualizo la pelicula"})
    
    
@movie_router.delete('/movies/', tags = [tasgs['MOVIES']], response_model = dict, status_code = 200)
def delete_movie(id: int) -> dict:
    db = Session()
    movie_find = db.query(movieModel).filter(movieModel.id == id).first()
    if not movie_find:        
        return JSONResponse(status_code=404, content= {"message": "Movie not found"})
    db.delete(movie_find)
    db.commit()
    return JSONResponse(status_code = 200, content={ "message": "se elimino la pelicula"})