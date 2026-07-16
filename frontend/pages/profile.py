import streamlit as st
import requests
from api.client import get_my_profile, get_my_reviews, get_error_message
from auth.state import require_login, clear_auth, current_profile, save_auth

require_login()
st.header("👤 Мой профиль")

profile = current_profile()
st.session_state.get(profile)

resp = get_my_profile()
if resp.ok:
    prof = resp.json()
    for k, v in prof.items():
        st.session_state["profile"][k] = v
    print(prof)
    save_auth(st.session_state.get("access_token"), profile)
else:
    st.error("Ошибка загрузки профиля")
    st.stop()

print(profile)

col1, col2 = st.columns([1, 2])

with col1:
    if profile.get("avatar_url"):
        st.image(profile["avatar_url"], width=150)
    else:
        st.image("https://via.placeholder.com/150x150?text=Аватар", width=150)

with col2:
    st.subheader(profile.get("username") or "Без никнейма")
    st.write(f"📧 {profile.get('email')}")
    st.write(f"🔑 Роль: {profile.get('role')}")
    if profile.get("bio"):
        st.write(f"📝 {profile.get('bio')}")

with st.expander("✏️ Редактировать профиль"):
    with st.form("edit_profile_form"):
        new_username = st.text_input("Никнейм", value=profile.get("username") or "")
        new_bio = st.text_area("Био", value=profile.get("bio") or "")
        new_avatar = st.text_input("Ссылка на аватарку", value=profile.get("avatar_url") or "")

        submitted = st.form_submit_button("Сохранить изменения")

        if submitted:
            payload = {}
            if new_username:
                payload["username"] = new_username
            if new_bio:
                payload["bio"] = new_bio
            if new_avatar:
                payload["avatar_url"] = new_avatar

            if payload:
                try:
                    from api.client import update_profile
                    resp = update_profile(payload)
                    if resp and resp.ok:
                        st.success("✅ Профиль обновлён!")
                        st.rerun()
                    else:
                        st.error(get_error_message(resp) if resp else "Ошибка")
                except Exception as e:
                    st.error(f"Ошибка: {e}")
            else:
                st.warning("Ничего не изменено")

st.divider()
st.subheader("📝 Мои отзывы")

try:
    resp = get_my_reviews()
    if resp.ok:
        reviews = resp.json()
        if reviews:
            for r in reviews:
                st.write(f"⭐ **{r['rating']}/10**")
                st.write(r["text"])
                st.caption(f"К фильму ID: {r.get('film_id')} | {r.get('created_at', '')[:10]}")
                st.divider()
        else:
            st.info("У вас пока нет отзывов")
    else:
        st.error("Ошибка загрузки отзывов")
except:
    st.error("Ошибка соединения")

st.divider()
if st.button("🚪 Выйти", type="primary"):
    clear_auth()
    st.switch_page("pages/login.py")