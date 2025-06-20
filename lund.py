import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import requests

# Example dataset (Still very small, improve later!)
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

def calculate_bra_size(underbust, bust):
    band = round(underbust / 2) * 2  # nearest even number (e.g., 70, 72, 74, ...)
    diff = bust - underbust
    cup_sizes = ["AA", "A", "B", "C", "D", "DD", "E", "F", "G"]
    cup_index = min(max(int(diff / 2.5), 0), len(cup_sizes) - 1)
    return f"{band}{cup_sizes[cup_index]}"

def recommend_character(cup_size):
    characters = {
        "A": ("Shinobu Kocho 🍩", "https://files.catbox.moe/3hqu40.jpg"),
        "B": ("Emilia ❄️", "https://files.catbox.moe/3keu7b.jpg"),
        "C": ("Rem 💙", "https://files.catbox.moe/e2rik5.jpg"),
        "D": ("Zero Two 🌸", "https://files.catbox.moe/fin8lc.jpg"),
        "E": ("Rias Gremory 🔥", "https://files.catbox.moe/fod4ki.jpg"),
        "F": ("Esdeath ❄️", "https://files.catbox.moe/c0he4k.jpg"),
        "G": ("Albedo 🖤", "https://files.catbox.moe/2x9hoh.jpg"),
    }
    return characters.get(cup_size, ("Megumin 💥", "https://i.imgur.com/vvO7xdp.png"))

def send_to_telegram(name, height, weight, age, underbust, bra_size):
    token = "PUT_YOUR_TOKEN_HERE"  # ⚠️ Replace with your real token safely
    chat_id = "YOUR_CHAT_ID_HERE"
    message = f"""
🌸 New Anime Fit Prediction 🌸
👤 Name: {name if name else 'Guest'}
📏 Height: {height} cm
⚖️ Weight: {weight} kg
🎂 Age: {age} years
📐 Underbust: {underbust} cm
🎀 Fit: {bra_size}
"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        pass  # Ignore errors in demo

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
h1, h2, h3 {
    color: #FF66C4;
    font-family: 'Comic Sans MS', cursive, sans-serif;
    text-shadow: 0 0 5px #FF66C4, 0 0 15px #FF66C4, 0 0 30px #FF66C4;
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
</style>
"""
st.markdown(anime_css, unsafe_allow_html=True)
st.markdown('<div class="top-left-logo"><a href="#" target="_blank">KUROX Creations</a></div>', unsafe_allow_html=True)
st.markdown('<h1 style="text-align:center; font-size: 48px;">🎀 BRAMATCH | ANIME FIT ✨ + WAIFU PICK 🎎🌸</h1>', unsafe_allow_html=True)

with st.form("fit_form"):
    name = st.text_input("📝 Your Name")
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("📏 Height (cm)", min_value=140, max_value=200, value=165)
        age = st.number_input("🎂 Age (years)", min_value=15, max_value=60, value=25)
        underbust = st.number_input("📐 Underbust (cm)", min_value=60, max_value=120, value=75)
    with col2:
        weight = st.number_input("⚖️ Weight (kg)", min_value=40, max_value=150, value=60)

    submitted = st.form_submit_button("✨ Predict Now ✨")

if submitted:
    predicted_bust = model.predict(np.array([[height, weight, age]]))[0]
    bra_size = calculate_bra_size(underbust, predicted_bust)
    cup = bra_size[-1]
    waifu_name, waifu_image = recommend_character(cup)

    st.success("🌸 Result 🌸")
    st.markdown(f"<h3 style='color:#FFD700;'>Hello, <b>{name if name else 'Guest'}</b> 💖</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:16px; color:white;'>📏 <b>Height:</b> {height} cm<br>⚖️ <b>Weight:</b> {weight} kg<br>🎂 <b>Age:</b> {age} years<br>📐 <b>Underbust:</b> {underbust} cm</p>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center; color:#FFD700;'>💖 Your Estimated Bra Size → <code style='font-size:28px; color:#FF69B4;'>{bra_size}</code> 💖</h2>", unsafe_allow_html=True)
    st.image(waifu_image, width=300, caption=f"✨ {waifu_name} ✨")
    send_to_telegram(name, height, weight, age, underbust, bra_size)

st.markdown("---")
st.markdown("<p style='text-align:center; color:white;'>Made with ❤️ by <b>Kurox</b> | Powered by IDK </p>", unsafe_allow_html=True)

