from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile import ProfileCreate, ProfileUpdate
from app.repositories.review_repository import ReviewRepository


class ProfileService:
    def __init__(self, db: Session):
        self.repo = ProfileRepository(db)

    def create_profile(self, user_id: int) -> dict:
        profile = Profile(
            user_id=user_id
        )

        return self.repo.create(profile)

    def get_profile_by_user(self, user_id: int) -> dict | None:
        profile = self.repo.get_by_user_id(user_id)
        if profile is None:
            return None

        return {
            "id": profile.id,
            "bio": profile.bio,
            "avatar_url": profile.avatar_url,
            "user_id": profile.user_id,
        }

    def update_profile(self, user_id: int, schema: ProfileUpdate) -> dict:
        profile = self.repo.get_by_user_id(user_id)
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )

        if schema.bio is not None:
            profile.bio = schema.bio
        if schema.avatar_url is not None:
            profile.avatar_url = schema.avatar_url

        profile = self.repo.update(profile)

        return {
            "id": profile.id,
            "bio": profile.bio,
            "avatar_url": profile.avatar_url,
            "user_id": profile.user_id,
        }

    def __init__(self, db: Session):
        self.repo = ProfileRepository(db)
        self.review_repo = ReviewRepository(db)

    def get_user_reviews(self, user_id: int) -> list[dict]:
        reviews = self.review_repo.get_by_user(user_id)
        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "created_at": r.created_at,
                "film_id": r.film_id,
            }
            for r in reviews
        ]