from pydantic import BaseModel
class Filmcreate(BaseModel):
    title: str
    description: str

class FilmResponse(BaseModel):
    id: int
    title: str
    description: str