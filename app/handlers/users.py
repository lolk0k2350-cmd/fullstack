from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user, require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse
from app.services.user_service import UserService
from app.services.review_service import ReviewService
from app.services.review_service import ReviewResponse

router = APIRouter(tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

def get_review_service(db: Session = Depends(get_db)) -> ReviewService:
        return ReviewService(db)


@router.get(
    "/users/me",
    response_model=UserResponse,
)
def get_my_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    "/admin/users",
    response_model=list[UserResponse],
)
def get_admin_users(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    service: UserService = Depends(get_user_service),
):
    return service.get_users()

@router.get(
    "/users/me/reviews",
    response_model=list[ReviewResponse],
)
def get_my_reviews(
    current_user: User = Depends(get_current_user),
    service: ReviewService = Depends(get_review_service),
):
    return service.get_reviews_by_user(current_user.id)