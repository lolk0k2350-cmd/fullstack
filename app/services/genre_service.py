from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.genre import Genre
from app.repositories.genre_repository import GenreRepository
from app.schemas.genre import GenreCreate, GenreUpdate


class GenreService:
    def __init__(self, db: Session):
        self.repo = GenreRepository(db)

    def create_genre(self, schema: GenreCreate) -> Genre:
        
        existing = self.repo.get_by_name(schema.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Genre with this name already exists",
            )

        genre = Genre(
            name=schema.name,
            description=schema.description,
        )
        return self.repo.create(genre)

    def get_genres(self) -> list[Genre]:
        return self.repo.get_all()

    def get_genre(self, genre_id: int) -> Genre:
        genre = self.repo.get_by_id(genre_id)
        if genre is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Genre not found",
            )
        return genre

    def update_genre(self, genre_id: int, schema: GenreUpdate) -> Genre:
        genre = self.get_genre(genre_id)

        if schema.name is None and schema.description is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        if schema.name is not None:
          
            existing = self.repo.get_by_name(schema.name)
            if existing and existing.id != genre_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Genre with this name already exists",
                )
            genre.name = schema.name

        if schema.description is not None:
            genre.description = schema.description

        return self.repo.update(genre)

    def delete_genre(self, genre_id: int) -> None:
        genre = self.get_genre(genre_id)
        self.repo.delete(genre)