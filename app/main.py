from fastapi import FastAPI

from app.api.health import router as health_router

from app.config.config import get_settings

from app.schemas.film import FilmCreate, FilmResponse

from app.database import Base, engine

from app.handlers.films import router as films_router
from app.handlers.genres import router as genres_router 

from app.models.film import Film


from app.database import Base, engine
settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(health_router)
@app.get("/")

def root():
    return {"message": f"{settings.app_name} is running"}


@app.post("/films", response_model=FilmResponse)
def create_film(film:FilmCreate):
    return {
        "id": 1,
        "title": film.title,
        "description": film.description,
    }



app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(films_router)
app.include_router(genres_router)  

@app.get("/")
def root():
    return {"message": "Hello World"}