import streamlit as st
from auth.state import is_authenticated, save_auth, clear_auth, is_admin
from api.client import get_profile
from cookies import get_cookie_controller

st.set_page_config(page_title="Кинотека", page_icon="🎬", layout="wide")

def restore_session():
    # Проверяем сначала куку, потом URL
    controller = get_cookie_controller()
    token = controller.get("access_token")
    
    if not token:
        token = st.query_params.get("token")
    
    if token and not is_authenticated():
        st.session_state["access_token"] = token
        try:
            resp = get_profile()
            if resp.ok:
                save_auth(token, resp.json())
            else:
                clear_auth()
        except:
            clear_auth()

restore_session()

pages = {
    "Каталог": [
        st.Page("pages/catalog.py", title="Фильмы"),
        st.Page("pages/details.py", title="Детали"),
        st.Page("pages/genres.py", title="Жанры"),
    ],
    "Пользователь": [
        st.Page("pages/profile.py", title="Профиль"),
    ],
    "Авторизация": [
        st.Page("pages/login.py", title="Вход"),
        st.Page("pages/registration.py", title="Регистрация"),
    ],
}

if is_admin():
    pages["Администратор"] = [
        st.Page("pages/create_film.py", title="Добавить фильм"),
        st.Page("pages/edit_film.py", title="Редактировать фильм"),
    ]

navigation = st.navigation(pages)
navigation.run()