from fastapi import FastAPI

from app.api.health import router as health_router
from app.config.config import get_settings

settings = get_settings()

app = FastAPI(
title=settings.app_name,
version=settings.app_version,
debug=settings.debug,
)

app.include_router(health_router)


@app.get("/")
def root():
    return {"message": f"{settings.app_name} is running"}

from app.schemas.film import Filmcreate, FilmResponse
@app.post("/films", response_model=FilmResponse)
def create_film(film: Filmcreate):
    return {
        "id": 1,
        "title": film.title,
        "description": film.description,
    }
