from pydantic import BaseModel, Field, ConfigDict

class GenreCreate(BaseModel):
    name: str
    description: str | None = None

class GenreResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    
class GenreUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)