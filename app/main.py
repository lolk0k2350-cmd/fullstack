from fastapi import FastAPI

import sys

from pathlib import Path

import uvicorn

from app.api.health import router as health_router

from app.config.config import get_settings

from app.schemas.film import FilmCreate, FilmResponse

from app.database import Base, engine

from app.handlers.films import router as films_router
from app.handlers.genres import router as genres_router 
from app.handlers.auth import router as auth_router
from app.handlers.users import router as users_router

from app.models.film import Film
from app.models.user import User
from app.models.genre import Genre

settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(films_router)
app.include_router(genres_router)  
app.include_router(users_router)
app.include_router(health_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": f"{settings.app_name} is running"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)


