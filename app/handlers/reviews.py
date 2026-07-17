from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate
from app.services.review_service import ReviewService

router = APIRouter(
    prefix="/films/{film_id}/reviews",
    tags=["reviews"],
)


def get_review_service(db: Session = Depends(get_db)) -> ReviewService:
    return ReviewService(db)


@router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_review(
    film_id: int,
    schema: ReviewCreate,
    current_user: User = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service),
):
    return service.create_review(schema, film_id, current_user.id)


@router.get(
    "/",
    response_model=list[ReviewResponse],
)
def get_reviews_by_film(
    film_id: int,
    service: ReviewService = Depends(get_review_service),
):
    return service.get_reviews_by_film(film_id)


@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
)
def get_review(
    review_id: int,
    service: ReviewService = Depends(get_review_service),
):
    return service.get_review(review_id)


@router.patch(
    "/{review_id}",
    response_model=ReviewResponse,
)
def update_review(
    review_id: int,
    schema: ReviewUpdate,
    current_user: User = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service),
):
    return service.update_review(review_id, schema, current_user.id)


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service),
):
    service.delete_review(review_id, current_user.id)