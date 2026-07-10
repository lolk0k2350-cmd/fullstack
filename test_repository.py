from app.database import Base, SessionLocal, engine
from app.models import Film, Genre
from app.repositories.film_repository import FilmRepository
from app.repositories.genre_repository import GenreRepository 

Base.metadata.create_all(bind=engine)

db = SessionLocal()


genre_repo = GenreRepository(db)
genre = Genre(name="Фантастика", description="Про космос")
genre_repo.create(genre)

film_repo = FilmRepository(db)
film = Film(title="Интерстеллар", description="Фильм про космос")
film.genres = [genre]
film_repo.create(film)

print(f"Фильм: {film.title} ({film.description})")
print(f"Жанры: {[g.name for g in film.genres]}")

db.close()