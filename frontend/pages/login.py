import streamlit as st
import requests
from api.client import login, get_profile, get_error_message
from auth.state import save_auth, clear_auth, is_authenticated

st.set_page_config(page_title="Вход", page_icon="🎬")

# ========== КРАСИВЫЙ ФОН С ЭФФЕКТОМ СТАРОГО КИНО ==========
st.markdown("""
<style>
    .stApp {
        background: #0a0a0a !important;
    }

    .stApp::after {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="1" stitchTiles="stitch"/></filter><rect width="100" height="100" filter="url(%23n)" opacity="0.04"/></svg>');
        pointer-events: none;
        z-index: 999;
        animation: flicker 0.15s infinite alternate;
    }
    @keyframes flicker {
        0% { opacity: 0.4; }
        100% { opacity: 0.7; }
    }

    .cinema-screen {
        max-width: 400px;
        margin: 60px auto;
        padding: 40px 30px;
        background: #111;
        border-radius: 20px;
        border: 2px solid rgba(255, 26, 26, 0.2);
        box-shadow: 0 0 60px rgba(255, 26, 26, 0.05);
        position: relative;
    }

    .stButton > button {
        background: #ff1a1a !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        letter-spacing: 2px !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    .stButton > button:hover {
        background: #cc0000 !important;
        box-shadow: 0 0 40px rgba(255, 26, 26, 0.3) !important;
    }

    .stTextInput > div > div > input {
        background: #1a1a1a !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 10px !important;
        color: white !important;
        padding: 14px 16px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #ff1a1a !important;
        box-shadow: 0 0 20px rgba(255, 26, 26, 0.1) !important;
    }

    h1 {
        color: #ff1a1a !important;
        font-size: 30px !important;
        text-align: center !important;
        letter-spacing: 6px !important;
        text-transform: uppercase !important;
        font-weight: 700 !important;
        margin-bottom: 5px !important;
        text-shadow: 0 0 30px rgba(255, 26, 26, 0.2);
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 12px;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 30px;
        font-weight: 300;
    }

    .register-link {
        text-align: center;
        margin-top: 20px;
        color: #555;
        font-size: 14px;
    }
    .register-link a {
        color: #ff1a1a !important;
        text-decoration: none;
        font-weight: 600;
    }
    .register-link a:hover {
        color: #ff6666 !important;
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, rgba(255, 26, 26, 0.3), transparent);
        margin: 25px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

if is_authenticated():
    st.info("Вы уже вошли.")
    st.switch_page("pages/catalog.py")

# ========== БЛОК ВХОДА ==========
st.markdown('<div class="cinema-screen">', unsafe_allow_html=True)

st.markdown("<h1>ВХОД</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Добро пожаловать</p>', unsafe_allow_html=True)
st.divider()

with st.form("login_form"):
    email = st.text_input("Email", placeholder="example@mail.ru")
    password = st.text_input("Пароль", type="password", placeholder="••••••••")
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
                st.error("❌ Бэкенд недоступен")

st.markdown("""
    <div class="register-link">
        Нет аккаунта? <a href="/registration">Зарегистрироваться</a>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)