from sqlalchemy.orm import Session
from app.models.review import Review


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, review: Review) -> Review:
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def get_by_id(self, review_id: int) -> Review | None:
        return self.db.query(Review).filter(Review.id == review_id).first()

    def get_by_film(self, film_id: int) -> list[Review]:
        return self.db.query(Review).filter(Review.film_id == film_id).all()

    def get_by_user(self, user_id: int) -> list[Review]:
        return self.db.query(Review).filter(Review.user_id == user_id).all()

    def update(self, review: Review) -> Review:
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def delete(self, review: Review) -> None:
        self.db.delete(review)
        self.db.commit()