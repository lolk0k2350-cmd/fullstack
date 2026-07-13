from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import List
from app.models.genre import Genre
from app.models.review import Review

film_genre = Table(
    "film_genre",
    Base.metadata,
    Column("film_id", ForeignKey("films.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)
class Film(Base):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    poster_url: Mapped[str] = mapped_column(String(500), nullable=True)

    genres: Mapped[list["Genre"]] = relationship(
        secondary=film_genre,
        back_populates="films",
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="film",
        cascade="all, delete-orphan",
    )