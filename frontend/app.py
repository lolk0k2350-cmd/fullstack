import streamlit as st
from auth.state import is_admin

st.set_page_config(page_title="Кинотека", page_icon="🎬", layout="wide")

pages = {
    "Каталог": [
        st.Page("pages/catalog.py", title="Фильмы", icon=":material/movie:", default=True),
        st.Page("pages/details.py", title="Детали", icon=":material/article:"),
        st.Page("pages/genres.py", title="Жанры", icon=":material/category:"),
    ],
    "Пользователь": [
        st.Page("pages/profile.py", title="Профиль", icon=":material/person:"),
            ],
    "Авторизация": [
        st.Page("pages/login.py", title="Вход", icon=":material/login:"),
        st.Page("pages/registration.py", title="Регистрация", icon=":material/person_add:"),
    ],
}

if is_admin():
    pages["Администратор"] = [
        st.Page("pages/create_film.py", title="Добавить фильм", icon=":material/add:"),
        st.Page("pages/edit_film.py", title="Редактировать фильм", icon=":material/edit:"),
    ]

navigation = st.navigation(pages)
navigation.run()