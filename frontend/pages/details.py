import streamlit as st
import requests
from api.client import get_film, get_reviews, create_review, get_error_message
from auth.state import is_authenticated
from components.star_rating import render_stars

film_id = st.session_state.get("selected_film_id")
if not film_id:
    st.warning("Фильм не выбран")
    st.stop()

try:
    film_resp = get_film(film_id)
    if film_resp.status_code != 200:
        st.error(get_error_message(film_resp))
        st.stop()
    film = film_resp.json()
except requests.RequestException:
    st.error("Ошибка загрузки")
    st.stop()

st.header(film["title"])
st.write(film.get("description", ""))
if film.get("genres"):
    st.write("**Жанры:** " + ", ".join([g["name"] for g in film["genres"]]))

if film.get("poster_url"):
    st.image(film["poster_url"], width=400)
else:
    st.image("https://via.placeholder.com/400x600?text=Нет+постера", width=400)

st.divider()
st.subheader("📝 Отзывы")

try:
    rev_resp = get_reviews(film_id)
    if rev_resp.status_code == 200:
        reviews = rev_resp.json()
        if reviews:
            for r in reviews:
                render_stars(r["rating"], max_rating=10, size=20)
                st.write(r["text"])
                st.divider()
        else:
            st.info("Пока нет отзывов")
    else:
        st.error(get_error_message(rev_resp))
except requests.RequestException:
    st.error("Ошибка загрузки отзывов")

if is_authenticated():
    with st.form("review_form"):
        rating = st.slider("Оценка", 1, 10, 5)
        text = st.text_area("Текст отзыва", placeholder="Напишите ваш отзыв...")
        submitted = st.form_submit_button("✉️ Отправить отзыв")

        if submitted:
            if text.strip():
                resp = create_review(film_id, text, rating)
                if resp.status_code == 201:
                    st.success("✅ Отзыв добавлен!")
                    st.rerun()
                else:
                    st.error(get_error_message(resp))
            else:
                st.error("Напишите текст")
else:
    st.warning("Авторизуйтесь, чтобы оставить отзыв")