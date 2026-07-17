import streamlit as st
import requests
from api.client import create_film, get_genres, get_error_message
from auth.state import require_admin

require_admin()
st.header("Добавить фильм")

try:
    resp = get_genres()
    genres = resp.json() if resp.status_code == 200 else []
except:
    genres = []

genre_options = {g["id"]: g["name"] for g in genres}

with st.form("create_film"):
    title = st.text_input("Название")
    description = st.text_area("Описание")
    selected_genres = st.multiselect("Жанры", options=genre_options.keys(), format_func=lambda x: genre_options.get(x, "Неизвестно"))
    submitted = st.form_submit_button("Создать")

if submitted:
    if not title:
        st.error("Укажите название")
    else:
        payload = {"title": title, "description": description, "genre_ids": selected_genres}
        resp = create_film(payload)
        if resp.status_code == 201:
            st.success("Фильм создан!")
            st.session_state["selected_film_id"] = resp.json()["id"]
            st.switch_page("pages/details.py")
        else:
            st.error(get_error_message(resp))