import streamlit as st
import requests
import random
from api.client import get_films, get_error_message
from components.film_card import render_film_card
from components.star_rating import render_small_stars
from auth.state import is_admin

st.header("🎬 Все фильмы")


try:
    resp = get_films()
    if resp.status_code == 200:
        films = resp.json()
        if films:
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button("🎲 Случайный фильм", use_container_width=True):
                    random_film = random.choice(films)
                    st.session_state["selected_film_id"] = random_film["id"]
                    st.switch_page("pages/details.py")
        else:
            films = []
    else:
        films = []
        st.error(get_error_message(resp))
except requests.RequestException:
    films = []
    st.error("❌ Бэкенд недоступен")


if is_admin() and st.button("➕ Добавить фильм"):
    st.switch_page("pages/create_film.py")


if films:
    cols = st.columns(3)
    for i, film in enumerate(films):
        with cols[i % 3]:
            render_film_card(film)
            if film.get("average_rating"):
                render_small_stars(film["average_rating"], max_rating=10, size=14)
else:
    st.info("Фильмов пока нет")