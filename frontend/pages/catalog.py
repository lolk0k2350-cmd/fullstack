import streamlit as st
import requests
from api.client import register, get_error_message

st.header("Регистрация")
with st.form("reg_form"):
    email = st.text_input("Email")
    password = st.text_input("Пароль", type="password")
    submitted = st.form_submit_button("Зарегистрироваться")

if submitted:
    if not email or not password:
        st.error("Заполните все поля")
    elif len(password) < 6:
        st.error("Пароль минимум 6 символов")
    else:
        try:
            resp = register(email, password)
            if resp.status_code == 201:
                st.success("Регистрация успешна! Теперь войдите.")
                st.switch_page("pages/login.py")
            else:
                st.error(get_error_message(resp))
        except requests.RequestException:
            st.error("недоступно")