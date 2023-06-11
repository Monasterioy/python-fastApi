from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from config.database import Session
from models.movie import Movie as movieModel
from services.movie import MovieService
from schema.movie import Movie

movie_router = APIRouter()

tasgs = {
    "MOVIES": "Movies",
}


@movie_router.get(
    "/movies", tags=[tasgs["MOVIES"]], response_model=List[Movie], status_code=200
)
def get_Movies() -> List[Movie]:
    db = Session()
    all_movies = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(all_movies))


@movie_router.get(
    "/movies/{id}", tags=[tasgs["MOVIES"]], response_model=Movie, status_code=200
)
def get_Movie(id: int = Path(le=2000, ge=0)) -> Movie:
    db = Session()
    movie_find = MovieService(db).get_movie(id)
    if not movie_find:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(movie_find))


@movie_router.get(
    "/movies/", tags=[tasgs["MOVIES"]], response_model=List[Movie], status_code=200
)
def get_movies_by_query(
    category: str = Query(max_length=15, min_length=5)
) -> List[Movie]:
    db = Session()
    movies = MovieService(db).get_movie_by_query(category)
    return JSONResponse(status_code=200, content=jsonable_encoder(movies))


@movie_router.post(
    "/movies/", tags=[tasgs["MOVIES"]], response_model=dict, status_code=201
)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "se registro la pelicula"})


@movie_router.put(
    "/movies/", tags=[tasgs["MOVIES"]], response_model=dict, status_code=200
)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    movie_find = MovieService(db).get_movie(id)
    if not movie_find:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(
        status_code=200, content={"message": "se actualizo la pelicula"}
    )


@movie_router.delete(
    "/movies/", tags=[tasgs["MOVIES"]], response_model=dict, status_code=200
)
def delete_movie(id: int) -> dict:
    db = Session()
    movie_find = MovieService(db).get_movie(id)
    if not movie_find:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": "se elimino la pelicula"})
