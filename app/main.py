from fastapi import FastAPI

from app.api.health import router as health_router

from app.config.config import settings

from app.schemas.film import FilmCreate, FilmResponse

from app.database import Base, engine

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
