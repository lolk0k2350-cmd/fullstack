import requests
from streamlit import session_state

BACKEND_URL = "http://127.0.0.1:8000"

def register(email, password):
    return requests.post(f"{BACKEND_URL}/auth/register", json={"email": email, "password": password})


def login(email, password):
    return requests.post(f"{BACKEND_URL}/auth/login", json={"email": email, "password": password})

def request_with_auth(method, endpoint, params=None, payload=None):
    headers = {"Authorization": f"Bearer {session_state['access_token']}"}
    if method == "GET":
        return requests.get(endpoint, headers=headers, params=params)
    elif method == "POST":
        return requests.post(endpoint, headers=headers, params=params, json=payload)
    elif method == "PATCH":
        return requests.patch(endpoint, headers=headers, params=params, json=payload)
    elif method == "DELETE":
        return requests.delete(endpoint, headers=headers, params=params)

def get_profile():
    return request_with_auth("GET", f"{BACKEND_URL}/users/me")

def get_my_reviews():
    return request_with_auth("GET", f"{BACKEND_URL}/users/me/reviews")

def get_my_profile():
    return request_with_auth("GET", f"{BACKEND_URL}/profile/me")

def update_profile(payload):
    return request_with_auth("PATCH", f"{BACKEND_URL}/profile/", payload=payload)

def get_films():
    return requests.get(f"{BACKEND_URL}/films")

def get_film(film_id):
    return requests.get(f"{BACKEND_URL}/films/{film_id}")

def create_film(payload):
    return request_with_auth("POST", f"{BACKEND_URL}/films", payload=payload)

def update_film(film_id, payload):
    return request_with_auth("PATCH", f"{BACKEND_URL}/films/{film_id}", payload=payload)

def delete_film(film_id):
    return request_with_auth("DELETE", f"{BACKEND_URL}/films/{film_id}")

def get_genres():
    return requests.get(f"{BACKEND_URL}/genres")

def create_genre(payload):
    return request_with_auth("POST", f"{BACKEND_URL}/genres", payload=payload)

def get_reviews(film_id):
    return requests.get(f"{BACKEND_URL}/films/{film_id}/reviews")

def create_review(film_id, text, rating):
    return request_with_auth("POST", f"{BACKEND_URL}/films/{film_id}/reviews", payload={"text": text, "rating": rating})

def get_profile():
    return request_with_auth("GET", f"{BACKEND_URL}/users/me")

def get_error_message(response):
    try:
        return response.json().get("detail", f"Ошибка HTTP {response.status_code}")
    except:
        return f"Ошибка HTTP {response.status_code}"