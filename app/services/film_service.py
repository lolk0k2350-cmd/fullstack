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

    def create_film(self, schema: FilmCreate) -> dict:
        genre_objects = []
        for genre_id in schema.genre_ids:
            genre = self.genre_repo.get_by_id(genre_id)
            if genre is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Genre with id {genre_id} not found",
                )
            genre_objects.append(genre)

        film = Film(
            title=schema.title,
            description=schema.description,
        )
        film.genres = genre_objects
        film = self.film_repo.create(film)

        return {
            "id": film.id,
            "title": film.title,
            "description": film.description,
            "genres": [
                {
                    "id": g.id,
                    "name": g.name,
                    "description": g.description
                }
                for g in film.genres
            ]
        }

    def get_films(self) -> list[dict]:
        films = self.film_repo.get_all()
        
        result = []
        for film in films:
            result.append({
                "id": film.id,
                "title": film.title,
                "description": film.description,
                "poster_url": film.poster_url,
                "genres": [
                    {
                        "id": g.id,
                        "name": g.name,
                        "description": g.description
                    }
                    for g in film.genres
                ]

            })
        return result

    def get_film(self, film_id: int) -> dict:
        film = self.film_repo.get_by_id(film_id)
        if film is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Film not found",
            )
        
        return {
            "id": film.id,
            "title": film.title,
            "description": film.description,
            "genres": [
                {
                    "id": g.id,
                    "name": g.name,
                    "description": g.description
                }
                for g in film.genres
            ]
        }

    def update_film(self, film_id: int, schema: FilmUpdate) -> dict:
        film = self.film_repo.get_by_id(film_id)
        if film is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Film not found",
            )

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
            genre_objects = []
            for genre_id in schema.genre_ids:
                genre = self.genre_repo.get_by_id(genre_id)
                if genre is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Genre with id {genre_id} not found",
                    )
                genre_objects.append(genre)
            film.genres = genre_objects

        film = self.film_repo.update(film)
        
        return {
            "id": film.id,
            "title": film.title,
            "description": film.description,
            "genres": [
                {
                    "id": g.id,
                    "name": g.name,
                    "description": g.description
                }
                for g in film.genres
            ]
        }

    def delete_film(self, film_id: int) -> None:
        film = self.film_repo.get_by_id(film_id)
        if film is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Film not found",
            )
        self.film_repo.delete(film)