import streamlit as st
import requests
from api.client import get_films, get_error_message
from components.film_card import render_film_card
from auth.state import is_admin

st.header("Все фильмы")
if is_admin() and st.button("Добавить фильм"):
    st.switch_page("pages/create_film.py")

try:
    resp = get_films()
    if resp.status_code == 200:
        films = resp.json()
        if films:
            cols = st.columns(3)
            for i, film in enumerate(films):
                with cols[i % 3]:
                    render_film_card(film)
        else:
            st.info("Фильмов пока нет")
    else:
        st.error(get_error_message(resp))
except requests.RequestException:
    st.error("недоступно")