import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import io
import textwrap

# --- 1. PRO APP CONFIG ---
st.set_page_config(page_title="Nadar: The 9th Light", page_icon="🕯️", layout="centered")

# Custom CSS for Golden Theme
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFD700; }
    .stButton>button {
        background: linear-gradient(to right, #CFAB50, #FBEF95, #CFAB50);
        color: #000000; font-weight: 900; border: 2px solid #FFD700;
        padding: 12px 25px; border-radius: 50px; letter-spacing: 1px;
        box-shadow: 0px 0px 20px rgba(255, 215, 0, 0.6);
    }
    .stTextInput>div>div>input {
        background-color: #111; color: #FFD700; text-align: center;
        border: 2px solid #FFD700; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ---
saloks_data = [
    {"text": "Chinta ta ki kijiye, jo anhoni hoye.", "mean": "Worry only about what is not destined to happen."},
    {"text": "Bhai kahu kau det neh, neh bhai manat aan.", "mean": "Fear none, and frighten none."},
    {"text": "Gun gobind gaiyo nahi, janam akarth keen.", "mean": "You have not sung His praises; life is wasted."},
    {"text": "Jo upjio so binas hai, paro aaj ke kaal.", "mean": "Whatever is created shall be destroyed."},
    {"text": "Bal chutkyo bandhan pare, kachu na hot upaaye.", "mean": "Strength is gone, only surrender saves you."},
    {"text": "Sang sakha sab taj gaye, kou na nibhyo saath.", "mean": "Friends left; only the Divine remains."},
    {"text": "Patit udharan bhay haran, sukh sagar narayan.", "mean": "He is the Destroyer of fear, Ocean of Peace."},
    {"text": "Ram simar ram simar, ihai tero kaaj hai.", "mean": "Remember the Lord; this is your only true work."},
]

# --- 3. PRO DESIGN ENGINE ---
def draw_glow_text(draw, text, x, y, font, text_color, glow_color="#C0A040", glow_radius=4):
    """Draws text with a rich golden glow effect."""
    # Mota Glow (Shadow)
    for off_x in range(-glow_radius, glow_radius+1):
        for off_y in range(-glow_radius, glow_radius+1):
            if off_x == 0 and off_y == 0: continue
            draw.text((x+off_x, y+off_y), text, font=font, fill=glow_color, anchor="mm")
    # Main Text (Sharp)
    draw.text((x, y), text, font=font, fill=text_color, anchor="mm")

def create_poster(name, data):
    try:
        # 1. Load & Darken Image (Cinematic Base)
        img = Image.open("background.jpg").convert("RGB")
        # Brightness kam karo taaki raat ka scene lage
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.5) # 50% Darker
        
        W, H = img.size
        draw = ImageDraw.Draw(img)

        # 2. Load Fonts (Mote Wale)
        try:
            font_large = ImageFont.truetype("font.ttf", int(H*0.085)) # Name (Sabse Bada)
            font_med = ImageFont.truetype("font.ttf", int(H*0.05))  # Salok
            font_small = ImageFont.truetype("font.ttf", int(H*0.028)) # Meaning & Footer
        except:
            font_large = ImageFont.load_default()
            font_med = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # 3. Draw Golden Border (Frame)
        border_thickness = int(W * 0.015)
        draw.rectangle(
            [border_thickness, border_thickness, W-border_thickness, H-border_thickness],
            outline="#FFD700", width=border_thickness
        )

        # 4. TEXT PLACEMENT (Upar Aasmaan Mein)
        
        # Name (Gold Glow)
        draw_glow_text(draw, name.upper(), W/2, H*0.16, font_large, "#FFD700")
        
        # Subtitle
        draw_glow_text(draw, "RECEIVED THE NADAR:", W/2, H*0.23, font_small, "#F0E0A0")

        # Salok (White Gold Glow)
        lines = textwrap.wrap(data['text'], width=20)
        y_text = H * 0.38
        for line in lines:
            draw_glow_text(draw, line, W/2, y_text, font_med, "#FFFFFF")
            y_text += int(H*0.065)

        # Meaning (Light Gold Glow)
        lines_mean = textwrap.wrap(data['mean'], width=30)
        y_mean = y_text + int(H*0.04)
        for line in lines_mean:
            draw_glow_text(draw, line, W/2, y_mean, font_small, "#FCEeb5")
            y_mean += int(H*0.04)

        # Footer (Branding)
        footer_y = H * 0.92
        draw_glow_text(draw, "350TH MARTYRDOM YEAR | GURU TEGH BAHADUR JI", W/2, footer_y, font_small, "#FFD700")
        draw_glow_text(draw, "DEV: KARAN (CHITKARA UNIV)", W/2, footer_y + int(H*0.035), font_small, "#888888", glow_color="black")

        return img
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- 4. UI ---
st.markdown("<h1 style='text-align: center; font-size: 3rem; color: #FFD700; text-shadow: 0px 0px 15px #FFD700;'>✨ NADAR ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaaaaa; letter-spacing: 1px;'>Receive Your Divine Blessing</p>", unsafe_allow_html=True)

name_input = st.text_input("ENTER YOUR NAME:", placeholder="E.g. Karan Singh")

if st.button("🌹 GET MY BLESSING 🌹", use_container_width=True):
    if name_input:
        sel = random.choice(saloks_data)
        img = create_poster(name_input, sel)
        
        if img:
            st.image(img, use_column_width=True)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=100)
            st.download_button("📥 DOWNLOAD HD POSTER", data=buf.getvalue(), file_name="Nadar_Blessing.jpg", mime="image/jpeg", use_container_width=True)
    else:
        st.warning("Please enter your name.")