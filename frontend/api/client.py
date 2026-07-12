import requests
from streamlit import session_state

BACKEND_URL = "http://127.0.0.1:8000"

LOGIN_ENDPOINT = f"{BACKEND_URL}/auth/login"
REGISTER_ENDPOINT = f"{BACKEND_URL}/auth/register"
PROFILE_ENDPOINT = f"{BACKEND_URL}/users/me"
FILMS_ENDPOINT = f"{BACKEND_URL}/films"
GENRES_ENDPOINT = f"{BACKEND_URL}/genres"


def register(email: str, password: str) -> requests.Response:
    return requests.post(REGISTER_ENDPOINT, json={"email": email, "password": password})


def login(email: str, password: str) -> requests.Response:
    return requests.post(LOGIN_ENDPOINT, json={"email": email, "password": password})


def request_with_auth(
    method: str,
    endpoint: str,
    params: dict | None = None,
    payload: dict | None = None,
) -> requests.Response:
    headers = {"Authorization": f"Bearer {session_state['access_token']}"}
    if method == "GET":
        return requests.get(endpoint, headers=headers, params=params)
    elif method == "POST":
        return requests.post(endpoint, headers=headers, params=params, json=payload)
    elif method == "PATCH":
        return requests.patch(endpoint, headers=headers, params=params, json=payload)
    elif method == "DELETE":
        return requests.delete(endpoint, headers=headers, params=params)
    raise ValueError("Неизвестный метод запроса")


def get_profile() -> requests.Response:
    return request_with_auth("GET", PROFILE_ENDPOINT)


def get_films() -> requests.Response:
    if session_state.get("access_token"):
        return request_with_auth("GET", FILMS_ENDPOINT)
    return requests.get(FILMS_ENDPOINT)


def get_film(film_id: int) -> requests.Response:
    endpoint = f"{FILMS_ENDPOINT}/{film_id}"
    if session_state.get("access_token"):
        return request_with_auth("GET", endpoint)
    return requests.get(endpoint)


def create_film(payload: dict) -> requests.Response:
    return request_with_auth("POST", FILMS_ENDPOINT, payload=payload)


def update_film(film_id: int, payload: dict) -> requests.Response:
    endpoint = f"{FILMS_ENDPOINT}/{film_id}"
    return request_with_auth("PATCH", endpoint, payload=payload)


def delete_film(film_id: int) -> requests.Response:
    endpoint = f"{FILMS_ENDPOINT}/{film_id}"
    return request_with_auth("DELETE", endpoint)


def get_genres() -> requests.Response:
    return requests.get(GENRES_ENDPOINT)


def get_reviews(film_id: int) -> requests.Response:
    endpoint = f"{FILMS_ENDPOINT}/{film_id}/reviews"
    return requests.get(endpoint)


def create_review(film_id: int, text: str, rating: int) -> requests.Response:
    endpoint = f"{FILMS_ENDPOINT}/{film_id}/reviews"
    return request_with_auth("POST", endpoint, payload={"text": text, "rating": rating})


def get_my_reviews() -> requests.Response:
    endpoint = f"{PROFILE_ENDPOINT}/reviews"
    return request_with_auth("GET", endpoint)


def get_error_message(response: requests.Response) -> str:
    try:
        detail = response.json().get("detail")
        return str(detail or f"Ошибка: HTTP {response.status_code}")
    except ValueError:
        return f"Ошибка: HTTP {response.status_code}"