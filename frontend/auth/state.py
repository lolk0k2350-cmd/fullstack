import streamlit as st
from cookies import get_cookie_controller

AUTH_COOKIE = "access_token"

def save_auth(token, profile):
    st.session_state["access_token"] = token
    st.session_state["profile"] = profile
    st.query_params["token"] = token

    controller = get_cookie_controller()
    controller.set(AUTH_COOKIE, token, path="/")

def clear_auth():
    st.session_state.pop("access_token", None)
    st.session_state.pop("profile", None)
    st.query_params.clear()

    controller = get_cookie_controller()
    controller.remove(AUTH_COOKIE, path="/")

def is_authenticated():
    return bool(st.session_state.get("access_token"))

def current_profile():
    return st.session_state.get("profile")


def is_admin():
    profile = current_profile()
    return profile and profile.get("role") == "admin"

def require_login():
    if is_authenticated():
        return
    st.warning("Сначала войдите в аккаунт.")
    if st.button("Перейти ко входу", key="require_login_button"):
        st.switch_page("pages/login.py")
    st.stop()

def require_admin():
    require_login()
    if not is_admin():
        st.error("Эта страница доступна только администратору.")
        st.stop()