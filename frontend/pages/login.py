import streamlit as st
import requests
from api.client import login, get_profile, get_error_message
from auth.state import save_auth, clear_auth, is_authenticated

st.header("🔐 Вход")

if is_authenticated():
    st.info("Вы уже вошли.")
    st.switch_page("pages/catalog.py")

with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")
    submitted = st.form_submit_button("Войти")

if submitted:
    if not email or not password:
        st.error("Заполните все поля")
    else:
        try:
            resp = login(email, password)
            if resp.status_code == 200:
                token = resp.json()["access_token"]
                st.session_state["access_token"] = token

                profile_resp = get_profile()
                if profile_resp.ok:
                    save_auth(token, profile_resp.json())
                    st.success("✅ Вход выполнен!")
                    st.switch_page("pages/catalog.py")
                else:
                    clear_auth()
                    st.error("Ошибка загрузки профиля")
            else:
                st.error(get_error_message(resp))
        except requests.RequestException:
            st.error("❌")