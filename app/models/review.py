from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.models.user import User

from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    text: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    film_id: Mapped[int] = mapped_column(ForeignKey("films.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    film: Mapped["Film"] = relationship(back_populates="reviews")
    user: Mapped["User"] = relationship(back_populates="reviews")