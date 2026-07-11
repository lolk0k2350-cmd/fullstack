from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class FilmCreate(BaseModel):
    title: str
    description: str
    genre_ids: list[int]  

class FilmResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None = None
    genres: list[dict]  
class FilmUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    genre_ids: list[int] | None = None