from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.genre import GenreCreate, GenreResponse, GenreUpdate
from app.services.genre_service import GenreService

router = APIRouter(
    prefix="/genres",
    tags=["genres"],
)

def get_genre_service(db: Session = Depends(get_db)) -> GenreService:
    return GenreService(db)

@router.post(
    "/",
    response_model=GenreResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_genre(
    schema: GenreCreate,
    service: GenreService = Depends(get_genre_service),
):
    return service.create_genre(schema)

@router.get(
    "/",
    response_model=list[GenreResponse],
)
def get_genres(
    service: GenreService = Depends(get_genre_service),
):
    return service.get_genres()

@router.get(
    "/{genre_id}",
    response_model=GenreResponse,
)
def get_genre(
    genre_id: int,
    service: GenreService = Depends(get_genre_service),
):
    return service.get_genre(genre_id)

@router.patch(
    "/{genre_id}",
    response_model=GenreResponse,
)
def update_genre(
    genre_id: int,
    schema: GenreUpdate,
    service: GenreService = Depends(get_genre_service),
):
    return service.update_genre(genre_id, schema)

@router.delete(
    "/{genre_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_genre(
    genre_id: int,
    service: GenreService = Depends(get_genre_service),
) -> None:
    service.delete_genre(genre_id)