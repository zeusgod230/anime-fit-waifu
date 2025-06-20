import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import requests

# ----------------------------
# Dataset (Demo Example)
# ----------------------------
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

# ----------------------------
# Helper Functions
# ----------------------------
def calculate_fit_label(bust_size):
    if bust_size < 80:
        return "XS"
    elif bust_size < 85:
        return "S"
    elif bust_size < 90:
        return "M"
    elif bust_size < 95:
        return "L"
    elif bust_size < 100:
        return "XL"
    else:
        return "XXL+"

def recommend_character(fit_label):
    characters = {
        "XS": ("Shinobu Kocho 🍩", "https://files.catbox.moe/3hqu40.jpg"),
        "S": ("Emilia ❄️", "https://files.catbox.moe/3keu7b.jpg"),
        "M": ("Rem 💙", "https://files.catbox.moe/e2rik5.jpg"),
        "L": ("Zero Two 🌸", "https://files.catbox.moe/fin8lc.jpg"),
        "XL": ("Rias Gremory 🔥", "https://files.catbox.moe/fod4ki.jpg"),
        "XXL+": ("Esdeath ❄️", "https://files.catbox.moe/c0he4k.jpg"),
    }
    return characters.get(fit_label, ("Megumin 💥", "https://i.imgur.com/vvO7xdp.png"))

def send_to_telegram(name, height, weight, age, fit_label):
    token = "7600751293:AAHsw7UlCgHweE7v5DATNNuVmx5h_0LdDzs"           # <-- Add your Bot token here
    chat_id = "7159587636"  # <-- Add your Telegram user ID here
    message = f"""
🌸 New Anime Fit Prediction 🌸
👤 Name: {name if name else 'Guest'}
📏 Height: {height} cm
⚖️ Weight: {weight} kg
🎂 Age: {age} years
🎀 Fit: {fit_label}
"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, data=payload)

st.set_page_config(page_title="🎀 BRAMATCH | ANIME FIT ✨ + WAIFU PICK 🎎🌸", page_icon="🌸", layout="centered")

anime_css = """
<style>
body {
    background-image: url('https://files.catbox.moe/mnkg4d.jpg');
    background-size: cover;
    background-attachment: fixed;
}
h1, h2, h3 {
    color: #FF66C4;
    font-family: 'Comic Sans MS', cursive, sans-serif;
}
.stButton>button {
    background-color: #FF69B4;
    color: white;
    border-radius: 10px;
    padding: 0.5rem 1.5rem;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #FF1493;
}
</style>
"""
st.markdown(anime_css, unsafe_allow_html=True)

# ----------------------------
# Title & Intro
# ----------------------------
st.markdown(
    """
    <h1 style="text-align:center; font-size: 48px;">🎀 BRAMATCH | ANIME FIT ✨ + WAIFU PICK 🎎🌸</h1>
    <p style="text-align:center; font-size:20px; color:white;">
        Fun ML demo! Estimate your outfit fit size and discover an inspiring anime character with similar energy ✨
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")


with st.form("fit_form"):
    name = st.text_input("📝 Your Name")
    col1, col2 = st.columns(2)

    with col1:
        height = st.number_input("📏 Height (cm)", min_value=140, max_value=200, value=165)
        age = st.number_input("🎂 Age (years)", min_value=15, max_value=60, value=25)

    with col2:
        weight = st.number_input("⚖️ Weight (kg)", min_value=40, max_value=150, value=60)

    submitted = st.form_submit_button("✨ Predict Now ✨")

# ----------------------------
# Prediction Output + Character Recommendation
# ----------------------------
if submitted:
    input_features = np.array([[height, weight, age]])
    predicted_bust = model.predict(input_features)[0]
    fit_label = calculate_fit_label(predicted_bust)
    character_name, character_image = recommend_character(fit_label)

    st.success("🌸 Result 🌸")

    st.markdown(
        f"""
        <h3 style='color:#FFD700;'>Hello, <b>{name if name else "Guest"}!</b> 💖</h3>
        <p style='font-size:16px; color:white;'>
            <b>Your Entered Info:</b><br>
            📏 Height: <code>{height} cm</code><br>
            ⚖️ Weight: <code>{weight} kg</code><br>
            🎂 Age: <code>{age} years</code><br>
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<h2 style='text-align:center; color:#FFD700;'>💖 Your Estimated Fit → <code style='font-size:28px; color:#FF69B4;'>{fit_label}</code> 💖</h2>",
        unsafe_allow_html=True,
    )

    st.caption("✨ This is just a fun estimation, actual sizes vary by brand and style.")

    st.markdown("---")
    st.markdown(f"<h2 style='text-align:center;'>🎎 Your Anime Inspiration 🎎</h2>", unsafe_allow_html=True)
    st.image(character_image, width=300, caption=f"✨ {character_name} ✨")

    # 📨 Send result to Telegram
    send_to_telegram(name, height, weight, age, fit_label)

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:white;'>Made with ❤️ by <b>Kurox</b> | Powered by Anime Universe</p>",
    unsafe_allow_html=True,
)
