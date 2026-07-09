from pydantic import BaseModel
from typing import Optional

class FilmCreate(BaseModel):
    title: str
    description: str
    genre_ids: list[int]  

class FilmResponse(BaseModel):
    id: int
    title: str
    description: str
    genres: list[dict]  