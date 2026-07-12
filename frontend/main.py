import streamlit as st
from streamlit import session_state
st.title("""Регистрация""")

st.subheader("Логин")
login=st.text_input("Логин", value = st.session_state.get("login"), placeholder="Введите логин...")

st.subheader("Пароль")
psw=st.text_input("Пароль", value = st.session_state.get("psw"), placeholder="Введите пароль...")

if st.button("Другая страница"):
    st.switch_page("pages/another.py")
st.session_state["login"]=login
st.session_state["psw"]=psw
st.text(f"Ваше имя: {login}")
st.text(f"Ваш пароль: {psw}")

