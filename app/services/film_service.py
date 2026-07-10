from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.film import Film
from app.models.genre import Genre
from app.repositories.film_repository import FilmRepository
from app.repositories.genre_repository import GenreRepository
from app.schemas.film import FilmCreate, FilmUpdate


class FilmService:
    def __init__(self, db: Session):
        self.film_repo = FilmRepository(db)
        self.genre_repo = GenreRepository(db)

    def create_film(self, schema: FilmCreate) -> Film:
        
        genres = []
        for genre_id in schema.genre_ids:
            genre = self.genre_repo.get_by_id(genre_id)
            if genre is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Genre with id {genre_id} not found",
                )
            genres.append(genre)

        film = Film(
            title=schema.title,
            description=schema.description,
        )
        film.genres = genres  
        return self.film_repo.create(film)

    def get_films(self) -> list[Film]:
        return self.film_repo.get_all()

    def get_film(self, film_id: int) -> Film:
        film = self.film_repo.get_by_id(film_id)
        if film is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Film not found",
            )
        return film

    def update_film(self, film_id: int, schema: FilmUpdate) -> Film:
        film = self.get_film(film_id)

        if schema.title is None and schema.description is None and schema.genre_ids is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        
        if schema.title is not None:
            film.title = schema.title
        if schema.description is not None:
            film.description = schema.description

        if schema.genre_ids is not None:
            genres = []
            for genre_id in schema.genre_ids:
                genre = self.genre_repo.get_by_id(genre_id)
                if genre is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Genre with id {genre_id} not found",
                    )
                genres.append(genre)
            film.genres = genres

        return self.film_repo.update(film)

    def delete_film(self, film_id: int) -> None:
        film = self.get_film(film_id)
        self.film_repo.delete(film)