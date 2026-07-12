from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.schemas.profile import ProfileCreate, ProfileResponse, ProfileUpdate
from app.services.profile_service import ProfileService
from app.schemas.review import ReviewResponse
from app.services.review_service import ReviewService


router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)


def get_profile_service(db: Session = Depends(get_db)) -> ProfileService:
    return ProfileService(db)
def get_review_service(db:Session = Depends(get_db)) -> ReviewService:
    return ReviewService(db)


@router.post(
    "/",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_profile(
    schema: ProfileCreate,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    return service.create_profile(current_user.id, schema)


@router.get(
    "/me",
    response_model=ProfileResponse,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    profile = service.get_profile_by_user(current_user.id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return profile


@router.patch(
    "/me",
    response_model=ProfileResponse,
)
def update_my_profile(
    schema: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    return service.update_profile(current_user.id, schema)

@router.get("/me/reviews")
def get_my_reviews(
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    return service.get_user_reviews(current_user.id)