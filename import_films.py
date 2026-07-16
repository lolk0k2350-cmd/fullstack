import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from pathlib import Path
from app.database import SessionLocal
from app.services.film_service import FilmService
from app.schemas.film import FilmCreate

JSON_FILE = Path("data/films.json")

def read_json(file_path: Path) -> list[dict]:
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def get_or_create_genre(db, genre_name):
    from app.models.genre import Genre
    genre = db.query(Genre).filter(Genre.name == genre_name).first()
    if not genre:
        genre = Genre(name=genre_name)
        db.add(genre)
        db.commit()
        db.refresh(genre)
    return genre

def import_films():
    films_data = read_json(JSON_FILE)
    db = SessionLocal()
    film_service = FilmService(db)

    created = 0
    errors = 0

    for film_data in films_data:
        try:
            genre_ids = []
            for genre_name in film_data.get("genres", []):
                genre = get_or_create_genre(db, genre_name)
                genre_ids.append(genre.id)

            film_create = FilmCreate(
                title=film_data["title"],
                description=film_data["description"],
                genre_ids=genre_ids,
                poster_url=film_data.get("poster_url"),  # 👈 СОХРАНЯЕМ ПОСТЕР
            )

            film_service.create_film(film_create)
            created += 1
            print(f"✅ Добавлен: {film_data['title']}")

        except Exception as e:
            errors += 1
            print(f"❌ Ошибка: {film_data.get('title')} — {e}")

    db.close()
    print(f"\n🎉 Добавлено: {created}, Ошибок: {errors}")

if __name__ == "__main__":
    import_films()