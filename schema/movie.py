from pydantic import BaseModel, Field
from typing import Optional


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(
        default="Mi pelicula",
        min_length=5,
        max_length=50,
    )
    category: str = Field(
        default="accion",
        min_length=5,
        max_length=12,
    )
    rating: float
    overview: str = Field(
        default="Descripcion de la pelicula",
        min_length=5,
        max_length=50,
    )
    year: int = Field(default=2023, le=2040)
