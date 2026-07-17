import streamlit as st
import requests
from api.client import get_genres, get_error_message

st.header("Жанры")
try:
    resp = get_genres()
    if resp.status_code == 200:
        genres = resp.json()
        if genres:
            for genre in genres:
                st.write(f"**{genre['name']}** — {genre.get('description', '')}")
        else:
            st.info("Жанров пока нет")
    else:
        st.error(get_error_message(resp))
except:
    st.error("Ошибка загрузки")