import streamlit as st
import requests
from api.client import get_my_profile, get_my_reviews, get_error_message
from auth.state import require_login, clear_auth

require_login()
st.header("Профиль")

try:
    resp = get_my_profile()
    if resp.ok:
        profile = resp.json()
        st.write(f"Email: {profile.get('email')}")
        st.write(f"Роль: {profile.get('role')}")
    else:
        st.error("Ошибка загрузки профиля")
except:
    st.error("Ошибка соединения")

st.divider()
st.subheader("Мои отзывы")
try:
    resp = get_my_reviews()
    if resp.ok:
        reviews = resp.json()
        if reviews:
            for r in reviews:
                st.write(f"⭐ {r['rating']}/10")
                st.write(r["text"])
                st.divider()
        else:
            st.info("У вас пока нет отзывов")
    else:
        st.error("Ошибка загрузки отзывов")
except:
    st.error("Ошибка соединения")

if st.button("Выйти"):
    clear_auth()
    st.switch_page("pages/login.py")