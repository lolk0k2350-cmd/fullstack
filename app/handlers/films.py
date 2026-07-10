from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.film import FilmCreate, FilmResponse, FilmUpdate
from app.services.film_service import FilmService

router = APIRouter(
    prefix="/films",
    tags=["films"],
)

def get_film_service(db: Session = Depends(get_db)) -> FilmService:
    return FilmService(db)

@router.post(
    "/",
    response_model=FilmResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_film(
    schema: FilmCreate,
    service: FilmService = Depends(get_film_service),
):
    return service.create_film(schema)

@router.get(
    "/",
    response_model=list[FilmResponse],
)
def get_films(
    service: FilmService = Depends(get_film_service),
):
    return service.get_films()

@router.get(
    "/{film_id}",
    response_model=FilmResponse,
)
def get_film(
    film_id: int,
    service: FilmService = Depends(get_film_service),
):
    return service.get_film(film_id)

@router.patch(
    "/{film_id}",
    response_model=FilmResponse,
)
def update_film(
    film_id: int,
    schema: FilmUpdate,
    service: FilmService = Depends(get_film_service),
):
    return service.update_film(film_id, schema)

@router.delete(
    "/{film_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_film(
    film_id: int,
    service: FilmService = Depends(get_film_service),
) -> None:
    service.delete_film(film_id)