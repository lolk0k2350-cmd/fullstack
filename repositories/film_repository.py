from sqlalchemy.orm import Session
from app.models.film import Film

class FilmRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, film: Film) -> Film:
        self.db.add(film)
        self.db.commit()
        self.db.refresh(film)
        return film
    def _upsert(self, film: Film) -> Film:
        self.db.add(film)
        self.db.commit()
        self.db.refresh(film)
        return film

    def get_all(self) -> list[Film]:
        return self.db.query(Film).all()

    def get_by_id(self, film_id: int) -> Film | None:
        return self.db.query(Film).filter(Film.id == film_id).first()

    def delete(self, film: Film) -> None:
        self.db.delete(film)
        self.db.commit()

    def update(self, film: Film) -> Film:
        self.db.add(film)
        self.db.commit()
        self.db.refresh(film)
        return film