from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class ReviewCreate(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    rating: int = Field(ge=1, le=10)


class ReviewUpdate(BaseModel):
    text: str | None = Field(default=None, min_length=1, max_length=5000)
    rating: int | None = Field(default=None, ge=1, le=10)


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    text: str
    rating: int
    created_at: datetime
    film_id: int
    user_id: int