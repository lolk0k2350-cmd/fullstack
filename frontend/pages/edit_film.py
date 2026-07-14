import streamlit as st
import requests
from api.client import get_film, update_film, get_genres, get_error_message
from auth.state import require_admin

require_admin()
st.header("Редактировать фильм")

film_id = st.session_state.get("edit_film_id")
if not film_id:
    st.warning("Фильм не выбран")
    st.stop()

try:
    film_resp = get_film(film_id)
    if film_resp.status_code != 200:
        st.error(get_error_message(film_resp))
        st.stop()
    film = film_resp.json()
except:
    st.error("Ошибка загрузки")
    st.stop()

try:
    resp = get_genres()
    all_genres = resp.json() if resp.status_code == 200 else []
except:
    all_genres = []

genre_options = {g["id"]: g["name"] for g in all_genres}
existing_genres = [g["id"] for g in film.get("genres", [])]

with st.form("edit_film"):
    title = st.text_input("Название", value=film["title"])
    description = st.text_area("Описание", value=film.get("description", ""))
    selected_genres = st.multiselect("Жанры", options=genre_options.keys(), format_func=lambda x: genre_options.get(x, "Неизвестно"), default=existing_genres)
    submitted = st.form_submit_button("Сохранить")

if submitted:
    if not title:
        st.error("Укажите название")
    else:
        payload = {"title": title, "description": description, "genre_ids": selected_genres}
        resp = update_film(film_id, payload)
        if resp.status_code == 200:
            st.success("Фильм обновлён!")
            st.session_state["selected_film_id"] = film_id
            st.switch_page("pages/details.py")
        else:
            st.error(get_error_message(resp))