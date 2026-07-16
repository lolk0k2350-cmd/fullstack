import streamlit as st
from api.client import delete_film, get_error_message
from auth.state import is_admin

def render_film_card(film):
    with st.container(border=True):
        st.subheader(film["title"])
        st.write(film.get("description", ""))
        if film.get("genres"):
            st.caption("Жанры: " + ", ".join([g["name"] for g in film["genres"]]))
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("Подробнее", key=f"details_{film['id']}"):
                st.session_state["selected_film_id"] = film["id"]
                st.switch_page("pages/details.py")
        if is_admin():
            with col2:
                if st.button("Удалить", key=f"del_{film['id']}"):
                    response = delete_film(film["id"])
                    if response.ok:
                        st.success("Фильм удалён!")
                        st.rerun()
                    else:
                        st.error(get_error_message(response))
        print(film.get("poster_url"))
        if film.get("poster_url"):
            st.image(film["poster_url"], width=200)
        else:
            st.image("https://via.placeholder.com/200x300?text=Нет+постера", width=200)