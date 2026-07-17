from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.models.user import User
from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile import ProfileCreate, ProfileUpdate


class ProfileService:
    def __init__(self, db: Session):
        self.profile_repo = ProfileRepository(db)

    def create_profile(self, schema: ProfileCreate, user: User) -> dict:
        existing = self.profile_repo.get_by_user_id(user.id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Profile already exists for this user",
            )

        profile = Profile(
            user_id=user.id,
            username=schema.username,
            bio=schema.bio,
            avatar_url=schema.avatar_url,
        )
        profile = self.profile_repo.create(profile)

        return {
            "id": profile.id,
            "user_id": profile.user_id,
            "username": profile.username,
            "bio": profile.bio,
            "avatar_url": profile.avatar_url,
        }

    def get_profile(self, user_id: int) -> dict:
        profile = self.profile_repo.get_by_user_id(user_id)
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )
        return {
            "id": profile.id,
            "user_id": profile.user_id,
            "username": profile.username,
            "bio": profile.bio,
            "avatar_url": profile.avatar_url,
        }

    def update_profile(self, schema: ProfileUpdate, user: User) -> dict:
        profile = self.profile_repo.get_by_user_id(user.id)
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )

        if schema.username is not None:
            profile.username = schema.username
        if schema.bio is not None:
            profile.bio = schema.bio
        if schema.avatar_url is not None:
            profile.avatar_url = schema.avatar_url

        profile = self.profile_repo.update(profile)

        return {
            "id": profile.id,
            "user_id": profile.user_id,
            "username": profile.username,
            "bio": profile.bio,
            "avatar_url": profile.avatar_url,
        }

    def delete_profile(self, user: User) -> None:
        profile = self.profile_repo.get_by_user_id(user.id)
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profile not found",
            )
        self.profile_repo.delete(profile)