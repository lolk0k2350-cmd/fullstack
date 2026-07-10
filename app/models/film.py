from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

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

    genres: Mapped[list["Genre"]] = relationship(
        secondary=film_genre,
        back_populates="films",
    )