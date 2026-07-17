from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.review import Review
from app.repositories.review_repository import ReviewRepository
from app.repositories.film_repository import FilmRepository
from app.repositories.user_repository import UserRepository
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse


class ReviewService:
    def __init__(self, db: Session):
        self.review_repo = ReviewRepository(db)
        self.film_repo = FilmRepository(db)
        self.user_repo = UserRepository(db)

    def create_review(self, schema: ReviewCreate, film_id: int, user_id: int) -> dict:
        
        film = self.film_repo.get_by_id(film_id)
        if film is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Film not found",
            )

        
        user = self.user_repo.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

       
        review = Review(
            text=schema.text,
            rating=schema.rating,
            film_id=film_id,
            user_id=user_id,
        )
        review = self.review_repo.create(review)

        
        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "created_at": review.created_at,
            "film_id": review.film_id,
            "user_id": review.user_id,
        }

    def get_reviews_by_film(self, film_id: int) -> list[dict]:
        reviews = self.review_repo.get_by_film(film_id)
        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "created_at": r.created_at,
                "film_id": r.film_id,
                "user_id": r.user_id,
            }
            for r in reviews
        ]

    def get_review(self, review_id: int) -> dict:
        review = self.review_repo.get_by_id(review_id)
        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )
        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "created_at": review.created_at,
            "film_id": review.film_id,
            "user_id": review.user_id,
        }

    def get_reviews_by_user(self, user_id: int) -> list[dict]:
        reviews = self.review_repo.get_by_user(user_id)
        return [
        {
            "id": r.id,
            "text": r.text,
            "rating": r.rating,
            "created_at": r.created_at,
            "film_id": r.film_id,
            "user_id": r.user_id,
        }
        for r in reviews
    ]

    def update_review(self, review_id: int, schema: ReviewUpdate, user_id: int) -> dict:
        review = self.review_repo.get_by_id(review_id)
        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )

        
        if review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit your own reviews",
            )

        if schema.text is not None:
            review.text = schema.text
        if schema.rating is not None:
            review.rating = schema.rating

        review = self.review_repo.update(review)

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "created_at": review.created_at,
            "film_id": review.film_id,
            "user_id": review.user_id,
        }

    def delete_review(self, review_id: int, user_id: int) -> None:
        review = self.review_repo.get_by_id(review_id)
        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )

        
        if review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own reviews",
            )

        self.review_repo.delete(review)