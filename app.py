import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import io
import textwrap
# --- IMPORT SECTION (Top pe hona chahiye) ---
import requests
from streamlit_lottie import st_lottie

# --- ANIMATION LOADER FUNCTION ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# --- CHOOSE YOUR ANIMATION (Jo pasand ho wo use karo) ---

# Option 1: Golden Diya (Candle Light) - BEST
url = "https://lottie.host/97067c91-6963-4bb3-8b47-a0d9f7300b4f/wc8X7s8M7k.json"

# Option 2: Golden Sparkles (Divine Feel) - Agar Diya na chale
url = "https://lottie.host/537e0954-2532-4599-9063-32df832b0227/2F7Z1q9Z9r.json"

# Option 3: Floating Lamp
# url = "https://assets10.lottiefiles.com/packages/lf20_w51pcehl.json"

lottie_anim = load_lottieurl(url)

# --- UI DISPLAY (Title ke upar lagana) ---
if lottie_anim:
    st_lottie(lottie_anim, height=150, key="anim_diya")
else:
    # Backup agar animation fail ho jaye
    st.markdown("<h1 style='text-align: center;'>🕯️</h1>", unsafe_allow_html=True) 

# --- 1. PRO CONFIG ---
st.set_page_config(page_title="Nadar: The 9th Light", page_icon="🕯️", layout="centered")

# --- MODERN UI CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFD700; }
    h1 {
        font-family: 'serif'; text-align: center; color: #FFD700;
        text-shadow: 0px 0px 25px #FFD700; font-size: 3.2rem !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #8E6E12, #F2D692, #8E6E12);
        color: black; font-weight: 900; border: none; padding: 15px 30px;
        border-radius: 50px; width: 100%; text-transform: uppercase; letter-spacing: 2px;
        box-shadow: 0px 0px 30px rgba(255, 215, 0, 0.4);
    }
    .stTextInput>div>div>input {
        background-color: #111; color: #FFD700; text-align: center;
        border: 1px solid #FFD700; border-radius: 10px; font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ---
saloks_data = [
    {"text": "Gun gobind gaiyo nahi, janam akarth keen.\nKahu nanak bhaj har mana, jih bidh jal kau meen.", 
     "mean": "You have not sung the Lord's praises; your life is wasted. Worship the Lord, just as the fish loves the water."},
    {"text": "Jo upjio so binas hai, paro aaj ke kaal.\nNanak har gun gai le, chaad sagal janjal.", 
     "mean": "Whatever is created shall be destroyed; understand this today. O Nanak, sing the Glorious Praises of the Lord."},
    {"text": "Bal chutkyo bandhan pare, kachu na hot upaaye.\nKahu nanak ab ot har, gaj jio hohu sahaaye.", 
     "mean": "Strength is gone, bonds are shackles. Says Nanak, the Lord is now my Support; He helps me as He helped the elephant."},
    {"text": "Sukh dukh jih parsai nahi, lobh moh abhiman.\nKahu nanak sun re mana, so murat bhagwan.", 
     "mean": "One who is not touched by pleasure or pain, greed, attachment, or pride—says Nanak, listen O mind, he is the very image of God."}
]

# --- 3. IMAGE ENGINE (FIXED FOOTER) ---
def draw_text_with_glow(draw, text, x, y, font, text_color, glow_color="black"):
    for off in [-2, -1, 1, 2]:
        draw.text((x+off, y), text, font=font, fill=glow_color, anchor="mm")
        draw.text((x, y+off), text, font=font, fill=glow_color, anchor="mm")
    draw.text((x, y), text, font=font, fill=text_color, anchor="mm")

def create_poster(name, data):
    try:
        img = Image.open("background.jpg").convert("RGBA")
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.4) # Darken
        W, H = img.size
        draw = ImageDraw.Draw(img)
        font_path = "font.ttf"

        # --- A. DIYA STICKER ---
        current_y = int(H * 0.05)
        try:
            diya = Image.open("diya.png").convert("RGBA")
            diya_w = int(W * 0.18)
            aspect = diya.height / diya.width
            diya_h = int(diya_w * aspect)
            diya = diya.resize((diya_w, diya_h))
            diya_x = (W - diya_w) // 2
            img.paste(diya, (diya_x, current_y), diya)
            current_y += diya_h + 25
        except:
            pass

        # --- B. NAME ---
        try: name_font = ImageFont.truetype(font_path, int(H*0.07))
        except: name_font = ImageFont.load_default()
        draw_text_with_glow(draw, name.upper(), W/2, current_y, name_font, "#FFD700")
        current_y += int(H * 0.05)

        # --- C. SUBTITLE ---
        try: sub_font = ImageFont.truetype(font_path, int(H * 0.02))
        except: sub_font = ImageFont.load_default()
        draw_text_with_glow(draw, "RECEIVED THE 9TH LIGHT:", W/2, current_y, sub_font, "#CCCCCC")
        current_y += int(H * 0.08)

        # --- D. SHABAD ---
        shabad_font_size = int(H * 0.035)
        try: shabad_font = ImageFont.truetype(font_path, shabad_font_size)
        except: shabad_font = ImageFont.load_default()
        lines = textwrap.wrap(data['text'], width=30)
        for line in lines:
            draw_text_with_glow(draw, line, W/2, current_y, shabad_font, "#FFFFFF")
            current_y += int(H * 0.045)
        current_y += 30

        # --- E. MEANING ---
        mean_font_size = int(H * 0.022)
        try: mean_font = ImageFont.truetype(font_path, mean_font_size)
        except: mean_font = ImageFont.load_default()
        lines_mean = textwrap.wrap(data['mean'], width=45)
        for line in lines_mean:
            draw_text_with_glow(draw, line, W/2, current_y, mean_font, "#FCEEB5")
            current_y += int(H * 0.03)

        # --- F. FOOTER (FIXED SIZE - CHHOTA KAR DIYA) ---
        # Font size 0.025 se ghata kar 0.018 kar diya taaki fit aaye
        try: foot_font = ImageFont.truetype(font_path, int(H * 0.018)) 
        except: foot_font = ImageFont.load_default()
        
        # Position ko bilkul bottom se thoda upar uthaya
        draw_text_with_glow(draw, "350TH MARTYRDOM YEAR | GURU TEGH BAHADUR JI", W/2, H*0.91, foot_font, "#FFD700")
        draw_text_with_glow(draw, "DEV: KARAN (CHITKARA UNIV)", W/2, H*0.94, foot_font, "#888888")

        # Border
        border = 20
        draw.rectangle([border, border, W-border, H-border], outline="#FFD700", width=6)

        return img.convert("RGB")
    except Exception as e:
        st.error(f"Image Error: {e}")
        return None

# --- 4. FRONTEND ---

# Lottie Animation Load Function
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# NEW WORKING LOTTIE URL (Golden Candle)
lottie_diya = load_lottieurl("https://lottie.host/97067c91-6963-4bb3-8b47-a0d9f7300b4f/wc8X7s8M7k.json")

if lottie_diya:
    st_lottie(lottie_diya, height=150, key="diya_anim")
else:
    st.markdown("<h1 style='text-align:center;'>🕯️</h1>", unsafe_allow_html=True)

st.markdown("<h1 style='margin-top: -10px;'>✨ NADAR ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888;'>Enter your name to receive a Complete Shabad</p>", unsafe_allow_html=True)

name_input = st.text_input(" ", placeholder="YOUR NAME (E.g. KARAN)")

if st.button("🌹 REVEAL MY BLESSING 🌹", use_container_width=True):
    if name_input:
        with st.spinner("Seeking blessings..."):
            sel = random.choice(saloks_data)
            img = create_poster(name_input, sel)
            if img:
                st.image(img, use_column_width=True)
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=95)
                st.download_button("📥 DOWNLOAD POSTER", data=buf.getvalue(), file_name=f"Nadar_{name_input}.jpg", mime="image/jpeg", use_container_width=True)
                st.balloons()
    else:
        st.warning("Please enter your name first.")