import streamlit as st
from auth.state import is_authenticated, save_auth, clear_auth, is_admin
from api.client import get_profile
from cookies import get_cookie_controller

st.set_page_config(page_title="Кинотека", page_icon="🎬", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
    }
    .stApp { background: #121212; color: #f0f0f0; }
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2 {
        color: #ff1a1a !important;
        font-weight: 700 !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        text-shadow: 0 0 30px rgba(255, 26, 26, 0.4);
    }

    .stButton > button {
        background: linear-gradient(135deg, #ff1a1a, #cc0000) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 30px rgba(255, 26, 26, 0.3);
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        box-shadow: 0 0 50px rgba(255, 26, 26, 0.6) !important;
        transform: scale(1.02);
        background: linear-gradient(135deg, #ff3333, #e60000) !important;
    }

    .stTextInput > div > div > input {
        background: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        padding: 12px 16px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #ff1a1a !important;
        box-shadow: 0 0 30px rgba(255, 26, 26, 0.2) !important;
    }
    .stTextInput > div > label {
        color: #ff9999 !important;
        font-weight: 600 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 12px !important;
    }

    /* ===== ГЛАВНОЕ — ПОЛЕ ДЛЯ ОТЗЫВА ===== */
    .stTextArea textarea {
        background: #1a1a1a !important;
        color: #ffffff !important;
        border: 2px solid #333 !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 16px !important;
    }
    .stTextArea textarea:focus {
        border-color: #ff1a1a !important;
        box-shadow: 0 0 20px rgba(255, 26, 26, 0.2) !important;
        background: #1a1a1a !important;
        color: #ffffff !important;
    }
    .stTextArea textarea::placeholder {
        color: #888 !important;
    }
    .stTextArea label {
        color: #ff9999 !important;
        font-weight: 600 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 12px !important;
    }

    .stSlider > div { color: #dddddd !important; }
    .stSlider > div > div { background: #333 !important; }
    .stSlider > div > div > div { background: #ff1a1a !important; }

    form p, form div, form span, form label { color: #dddddd !important; }

    .stContainer {
        background: #1a1a1a !important;
        border-radius: 16px !important;
        border: 1px solid #2a2a2a !important;
        padding: 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }
    .stContainer:hover {
        border-color: #ff1a1a !important;
        box-shadow: 0 0 40px rgba(255, 26, 26, 0.15) !important;
        transform: translateY(-5px);
        background: #242424 !important;
    }
    .stContainer h3 { color: #ffffff !important; }
    .stContainer p, .stContainer div { color: #cccccc !important; }
    .stContainer .stCaption {
        color: #ffd700 !important;
        font-weight: 600 !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f0f, #1a0a0a) !important;
        border-right: 2px solid rgba(255, 26, 26, 0.2) !important;
        box-shadow: 4px 0 40px rgba(0, 0, 0, 0.6) !important;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: #ff1a1a !important;
        text-shadow: 0 0 30px rgba(255, 26, 26, 0.3) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] div {
        color: #dddddd !important;
    }
    section[data-testid="stSidebar"] .stPageLink {
        color: #dddddd !important;
        transition: all 0.3s ease !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] .stPageLink:hover {
        background: rgba(255, 26, 26, 0.1) !important;
        color: #ffffff !important;
        border-left: 3px solid #ff1a1a !important;
        padding-left: 20px !important;
    }
    section[data-testid="stSidebar"] .stPageLink[aria-current="page"] {
        background: rgba(255, 26, 26, 0.15) !important;
        color: #ffffff !important;
        border-left: 3px solid #ff1a1a !important;
        box-shadow: 0 0 30px rgba(255, 26, 26, 0.1) !important;
    }
    section[data-testid="stSidebar"] hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, rgba(255, 26, 26, 0.3), transparent) !important;
        margin: 20px 0 !important;
    }

    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #ff1a1a, transparent);
        margin: 30px 0;
        box-shadow: 0 0 30px rgba(255, 26, 26, 0.3);
    }

    .stSuccess { background: rgba(0, 200, 0, 0.1) !important; border-left: 4px solid #00ff00 !important; color: #00ff00 !important; }
    .stError { background: rgba(255, 0, 0, 0.1) !important; border-left: 4px solid #ff1a1a !important; color: #ff1a1a !important; }
    .stWarning { background: rgba(255, 215, 0, 0.05) !important; border-left: 4px solid #ffd700 !important; color: #ffd700 !important; }
    .stInfo { background: rgba(0, 100, 255, 0.05) !important; border-left: 4px solid #4488ff !important; color: #4488ff !important; }

    .stImage {
        border-radius: 10px !important;
        border: 2px solid #333 !important;
        transition: all 0.3s ease;
    }
    .stImage:hover { border-color: #ffd700 !important; box-shadow: 0 0 40px rgba(255, 215, 0, 0.2); }

    .streamlit-expanderHeader {
        color: #ff1a1a !important;
        font-weight: 700 !important;
        background: #1a1a1a !important;
        border-radius: 8px !important;
        border: 1px solid #2a2a2a !important;
        transition: all 0.3s ease;
    }
    .streamlit-expanderHeader:hover { border-color: #ff1a1a !important; background: #242424 !important; }

    .gold-star { color: #ffd700; font-size: 24px; text-shadow: 0 0 30px rgba(255, 215, 0, 0.4); }
    .empty-star { color: #444; font-size: 24px; }

    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(ellipse at center, transparent 65%, rgba(0,0,0,0.3) 100%);
        pointer-events: none;
        z-index: 0;
    }
    .stApp > div { position: relative; z-index: 1; }
</style>
""", unsafe_allow_html=True)

def restore_session():
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
        st.Page("pages/details.py", title="Подробнее"),
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