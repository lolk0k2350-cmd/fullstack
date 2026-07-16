import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from pathlib import Path
from app.database import SessionLocal
from app.models.film import Film

JSON_FILE = Path("data/films.json")

def update_posters():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        films_data = json.load(f)

    db = SessionLocal()
    updated = 0

    for film_data in films_data:
        title = film_data.get("title")
        poster_url = film_data.get("poster_url")

        if not title or not poster_url:
            continue

        film = db.query(Film).filter(Film.title == title).first()
        if film:
            film.poster_url = poster_url
            updated += 1
            print(f"✅ {title} — постер обновлён")

    db.commit()
    db.close()
    print(f"\n🎉 Обновлено постеров: {updated}")

if __name__ == "__main__":
    update_posters()