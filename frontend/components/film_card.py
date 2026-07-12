import requests
import streamlit as st
from api.client import delete_film, get_error_message
from auth.state import is_admin


def render_film_card(film: dict) -> None:
    with st.container(border=True):
        st.subheader(film["title"])
        st.write(film.get("description", ""))

        if film.get("genres"):
            genre_names = [g["name"] for g in film["genres"]]
            st.caption("Жанры: " + ", ".join(genre_names))
        else:
            st.caption("Жанры не указаны")

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            if st.button("Подробнее", key=f"details_{film['id']}"):
                st.session_state["selected_film_id"] = film["id"]
                st.switch_page("pages/details.py")

        if is_admin():
            with col2:
                if st.button("Редактировать", key=f"edit_{film['id']}"):
                    st.session_state["edit_film_id"] = film["id"]
                    st.switch_page("pages/edit_film.py")

            with col3:
                if st.button("Удалить", key=f"delete_{film['id']}", type="primary"):
                    try:
                        response = delete_film(film["id"])
                        if response.ok:
                            st.success("Фильм удалён!")
                            st.rerun()
                        else:
                            st.error(get_error_message(response))
                    except requests.RequestException:
                        st.error("Ошибка соединения")