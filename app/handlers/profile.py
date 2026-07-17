from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.schemas.profile import ProfileCreate, ProfileResponse, ProfileUpdate
from app.services.profile_service import ProfileService
from app.schemas.review import ReviewResponse
from app.services.review_service import ReviewService
from app.models.profile import Profile

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
@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(
    schema: ProfileCreate,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    return service.create_profile(schema, current_user)

@router.get(
    "/me",
    response_model=ProfileResponse,
)
def get_profile(
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    return service.get_profile(current_user.id)


@router.patch("/")
def update_my_profile(
    schema: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
):
    return service.update_profile(schema, current_user)  # 👈 ПРАВИЛЬНЫЙ ПОРЯДОК