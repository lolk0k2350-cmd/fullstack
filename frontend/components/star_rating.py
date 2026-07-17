import streamlit as st

def render_stars(rating, max_rating=10, size=20):
    
    filled = int(round(rating))
    empty = max_rating - filled
    
    stars_html = ""
    for i in range(filled):
        stars_html += f'<span class="gold-star" style="font-size:{size}px;">★</span>'
    for i in range(empty):
        stars_html += f'<span class="empty-star" style="font-size:{size}px;">★</span>'
    
    st.markdown(
        f'{stars_html} <span style="color:#aaa;font-size:{size-4}px;margin-left:8px;">{rating}/10</span>',
        unsafe_allow_html=True
    )

def render_small_stars(rating, max_rating=10, size=14):
    
    filled = int(round(rating))
    empty = max_rating - filled
    
    stars = ""
    for i in range(filled):
        stars += f'<span style="color:#ffd700;font-size:{size}px;">★</span>'
    for i in range(empty):
        stars += f'<span style="color:#444;font-size:{size}px;">★</span>'
    
    st.markdown(stars, unsafe_allow_html=True)

































































































































































