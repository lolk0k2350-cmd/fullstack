from sqlalchemy.orm import Session
from app.models.genre import Genre

class GenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, genre: Genre) -> Genre:
        self.db.add(genre)
        self.db.commit()
        self.db.refresh(genre)
        return genre

    def get_all(self) -> list[Genre]:
        return self.db.query(Genre).all()

    def get_by_id(self, genre_id: int) -> Genre | None:
        return self.db.query(Genre).filter(Genre.id == genre_id).first()
    
    def get_by_name(self, name: str) -> Genre | None:
        return self.db.query(Genre).filter(Genre.name == name).first()
    
    def delete(self, film: Genre) -> None:
        self.db.delete(Genre)
        self.db.commit()

    def update(self, genre: Genre) -> Genre:
        self.db.add(genre)
        self.db.commit()
        self.db.refresh(genre)
        return genre