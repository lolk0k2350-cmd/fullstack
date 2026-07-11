from pydantic import BaseModel, ConfigDict, Field


class ProfileCreate(BaseModel):
    bio: str | None = Field(default=None, max_length=1000)
    avatar_url: str | None = Field(default=None, max_length=500)


class ProfileUpdate(BaseModel):
    bio: str | None = Field(default=None, max_length=1000)
    avatar_url: str | None = Field(default=None, max_length=500)


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    bio: str | None = None
    avatar_url: str | None = None
    user_id: int