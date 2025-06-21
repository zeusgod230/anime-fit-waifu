import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import requests
import os
from dotenv import load_dotenv

load_dotenv()

data = {
    'height': [150, 155, 160, 165, 170, 175, 180],
    'weight': [45, 50, 55, 60, 65, 70, 75],
    'age': [18, 20, 22, 24, 26, 28, 30],
    'bust_size_cm': [80, 83, 86, 89, 92, 95, 98]
}
df = pd.DataFrame(data)

X = df[['height', 'weight', 'age']]
y = df['bust_size_cm']
model = LinearRegression()
model.fit(X, y)

# ✅ Indian realistic bra sizing logic
def cm_to_bra_size(cm):
    band_sizes = [30, 32, 34, 36, 38]
    estimated_underbust = cm * 0.8
    closest_band = min(band_sizes, key=lambda x: abs(x - estimated_underbust))

    diff = cm - closest_band
    if diff <= 1:
        cup = "A"
    elif diff <= 3:
        cup = "B"
    elif diff <= 5:
        cup = "C"
    elif diff <= 7:
        cup = "D"
    else:
        cup = "DD"
    return f"{closest_band}{cup}"

# ✅ Anime based on BMI → realistic spread
def recommend_character(height, weight):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    if bmi < 18.5:
        return ("Shinobu Kocho 🍩", "https://files.catbox.moe/3hqu40.jpg")
    elif 18.5 <= bmi < 22:
        return ("Emilia ❄️", "https://files.catbox.moe/3keu7b.jpg")
    elif 22 <= bmi < 25:
        return ("Rem 💙", "https://files.catbox.moe/e2rik5.jpg")
    elif 25 <= bmi < 28:
        return ("Zero Two 🌸", "https://files.catbox.moe/fin8lc.jpg")
    else:
        return ("Rias Gremory 🔥", "https://files.catbox.moe/fod4ki.jpg")


def send_to_telegram(name, height, weight, age, bra_size):
    token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")

    message = f"""
🌸 New Anime Fit Prediction 🌸
👤 Name: {name if name else 'Guest'}
📏 Height: {height} cm
⚖️ Weight: {weight} kg
🎂 Age: {age} years
🎀 Fit: {bra_size}
"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, data=payload)

st.set_page_config(page_title="🎀 BRAMATCH | ANIME FIT ✨ + WAIFU PICK 🎎🌸", page_icon="🌸", layout="centered")

anime_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://files.catbox.moe/mnkg4d.jpg');
    background-size: cover;
    background-attachment: fixed;
}
[data-testid="stSidebar"] {
    background-color: transparent;
}
.top-left-logo {
    position: absolute;
    top: 15px;
    left: 15px;
    z-index: 999;
    font-size: 18px;
    color: #fff;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    text-shadow: 0 0 10px #FF66C4, 0 0 20px #FF66C4;
}
.top-left-logo a {
    text-decoration: none;
    color: red;
    font-weight: bold;
    text-shadow: 2px 2px 5px black, 0 0 10px #ff0000, 0 0 20px #ff0000;
    font-size: 22px;
}
.glow-title {
    text-align: center;
    font-size: 52px;
    color: #ffff00;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    text-shadow:
        0 0 10px #ff66ff,
        0 0 20px #ff66ff,
        0 0 30px #ff66ff,
        0 0 40px #ff33ff,
        0 0 50px #ff00ff,
        0 0 60px #ff00ff,
        0 0 80px #ff00ff;
    padding: 1rem;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.07);
    border: 2px solid #ff99ff;
}
.glass {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2.5rem;
    backdrop-filter: blur(60px);
    -webkit-backdrop-filter: blur(30px);
    border: 1px solid rgba(255, 255, 255, 0.25);
    box-shadow: 0 8px 40px rgba(255, 105, 180, 0.5);
    margin: 2rem auto;
    width: 90%;
    max-width: 700px;
}
h1, h2, h3 {
    color: #FF66C4;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    text-shadow:
        0 0 5px #FF66C4,
        0 0 15px #FF66C4,
        0 0 30px #FF66C4;
}
.stButton>button {
    background-color: #FF69B4;
    color: white;
    border-radius: 12px;
    padding: 0.6rem 2rem;
    font-weight: bold;
    transition: all 0.3s ease;
    font-size: 18px;
}
.stButton>button:hover {
    background-color: #e60073;
    box-shadow: 0 0 15px #ff66c4, 0 0 30px #ff66c4, 0 0 60px #ff66c4;
}
.waifu-caption {
    text-align: center;
    font-size: 26px;
    color: #ffff00;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    text-shadow:
        0 0 10px #ff99ff,
        0 0 20px #ff66ff,
        0 0 30px #ff33ff,
        0 0 40px #ff00ff,
        0 0 60px #ff00ff;
    margin-top: 0.8rem;
}
</style>
"""
st.markdown(anime_css, unsafe_allow_html=True)

st.markdown('<div class="top-left-logo"><a href="#" target="_blank">KUROX Creations</a></div>', unsafe_allow_html=True)

st.markdown("""
<h1 style="text-align:center; font-size: 48px;">🎀 BRAMATCH | ANIME FIT ✨ + WAIFU PICK 🎎🌸</h1>
<p style="text-align:center; font-size:20px; color:white;">
       Welcome! This is a playful anime-inspired bra size predictor powered by ML.<br>
It’s just for fun and meant to entertain. No offense intended—thank you for understanding! ✨💖
</p>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<style>
.big-neon-thanks {
    font-family: 'Comic Sans MS', cursive, sans-serif;
    color: #ffff66;
    text-align: center;
    font-size: 60px;
    text-shadow:
        0 0 15px #ff99ff,
        0 0 30px #ff99ff,
        0 0 45px #ff99ff,
        0 0 60px #ff99ff,
        0 0 75px #ff99ff;
    margin-top: 2rem;
    margin-bottom: 2rem;
    padding: 0.5rem;
}
</style>
<div class="big-neon-thanks">Thanks for using this 💖</div>
""", unsafe_allow_html=True)

with st.form("fit_form"):
    name = st.text_input("📝 Your Name")
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("📏 Height (cm)", min_value=140, max_value=200, value=165, step=1)
        age = st.number_input("🎂 Age (years)", min_value=15, max_value=60, value=25, step=1)
    with col2:
        weight = st.number_input("⚖️ Weight (kg)", min_value=40, max_value=150, value=60, step=1)
    submitted = st.form_submit_button("✨ Predict Now ✨")

if submitted:
    input_features = np.array([[height, weight, age]])
    predicted_bust = model.predict(input_features)[0]
    bra_size = cm_to_bra_size(predicted_bust)
    character_name, character_image = recommend_character(height, weight)

    st.success("🌸 Result 🌸")
    st.markdown(f"""
        <h3 style='color:#FFD700;'>Hello, <b>{name if name else "Guest"}!</b> 💖</h3>
        <p style='font-size:16px; color:white;'>
            <b>Your Entered Info:</b><br>
            📏 Height: <code>{height} cm</code><br>
            ⚖️ Weight: <code>{weight} kg</code><br>
            🎂 Age: <code>{age} years</code><br>
        </p>
        """, unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center; color:#FFD700;'>💖 Your Estimated Fit → <code style='font-size:28px; color:#FF69B4;'>{bra_size}</code> 💖</h2>", unsafe_allow_html=True)
    st.caption("✨ This is just a fun estimation, actual sizes vary by brand and style.")
    st.markdown("---")
    st.markdown(f"<h2 style='text-align:center;'>🎎 Your Anime Inspiration 🎎</h2>", unsafe_allow_html=True)
    st.image(character_image, width=300, caption=f"✨ {character_name} ✨")

    send_to_telegram(name, height, weight, age, bra_size)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<p style='text-align:center; color:white;'>Made with ❤️ by <b>Kurox</b> | Powered by IDK </p>", unsafe_allow_html=True)

