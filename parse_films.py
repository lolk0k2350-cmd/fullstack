import json
import requests
from pathlib import Path

API_TOKEN = "5b3b806d-ab25-46d0-b8b4-4bfab210b274"
SEARCH_QUERY = "холоп"

OUTPUT_FILE = Path("data/films.json")

HEADERS = {
    "X-API-KEY": API_TOKEN,
    "Content-Type": "application/json"
}

def search_films(query: str, page: int = 1) -> dict:
    url = "https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword"
    params = {"keyword": query, "page": page}
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def parse_films(data: dict) -> list[dict]:
    films = []
    for item in data.get("films", []):
        film = {
            "title": item.get("nameRu") or item.get("nameEn") or "Без названия",
            "description": item.get("description") or "Описание отсутствует",
            "year": item.get("year"),
            "poster_url": item.get("posterUrl") or item.get("posterUrlPreview"),
            "genres": [genre["genre"] for genre in item.get("genres", [])],
            "rating": item.get("rating"),
        }
        films.append(film)
    return films

def save_to_json(films: list[dict], file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(films, f, ensure_ascii=False, indent=4)

def main():
    print(f"🔍 Ищем фильмы по запросу '{SEARCH_QUERY}'...")
    response_data = search_films(SEARCH_QUERY)
    films = parse_films(response_data)
    save_to_json(films, OUTPUT_FILE)
    print(f"✅ Сохранено {len(films)} фильмов в {OUTPUT_FILE}")

if __name__ == "__main__":
    main()