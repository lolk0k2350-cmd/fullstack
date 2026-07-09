from pydantic import BaseModel

class GenreCreate(BaseModel):
    name: str
    description: str | None = None

class GenreResponse(BaseModel):
    id: int
    name: str
    description: str | None = None