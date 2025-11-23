import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import io
import textwrap

# --- 1. APP SETUP ---
st.set_page_config(page_title="Nadar: The 9th Light", page_icon="🕯️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFD700; }
    .stButton>button {
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        color: black; font-weight: bold; border: none; padding: 12px 25px; border-radius: 50px;
        box-shadow: 0px 0px 15px #FFD700;
    }
    .stTextInput>div>div>input { text-align: center; border: 2px solid #FFD700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ---
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

# --- 3. DESIGN ENGINE (CINEMATIC) ---
def add_glow_text(draw, text, x, y, font, text_color="white", glow_color="black"):
    # Mota Shadow (Glow Effect)
    for off in [-3, -2, -1, 1, 2, 3]:
        draw.text((x+off, y), text, font=font, fill=glow_color, anchor="mm")
        draw.text((x, y+off), text, font=font, fill=glow_color, anchor="mm")
    # Main Text
    draw.text((x, y), text, font=font, fill=text_color, anchor="mm")

def create_poster(name, data):
    try:
        # 1. Load & Darken Image (Cinematic Effect)
        img = Image.open("background.jpg").convert("RGB")
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.6) # Image ko 40% Dark kar diya taki text chamke
        
        W, H = img.size
        draw = ImageDraw.Draw(img)

        # 2. Load Fonts (Strict Check)
        try:
            font_large = ImageFont.truetype("font.ttf", int(H*0.07)) # Name
            font_med = ImageFont.truetype("font.ttf", int(H*0.045))  # Salok
            font_small = ImageFont.truetype("font.ttf", int(H*0.025)) # Meaning
        except:
            st.error("🚨 FONT ERROR: 'font.ttf' nahi mila! Default use ho raha hai jo ganda dikhega.")
            return None # Ganda poster mat dikhao, error dikhao

        # 3. Draw Golden Border
        border_w = 20
        draw.rectangle([border_w, border_w, W-border_w, H-border_w], outline="#FFD700", width=10)

        # 4. TEXT PLACEMENT (Uppar Aasmaan Mein)
        
        # Name (Gold)
        add_glow_text(draw, name.upper(), W/2, H*0.15, font_large, "#FFD700", "black")
        
        # "Received the Nadar"
        add_glow_text(draw, "received the Nadar:", W/2, H*0.21, font_small, "#CCCCCC", "black")

        # Salok (White & Big)
        lines = textwrap.wrap(data['text'], width=20)
        y_text = H * 0.35 # Building se upar rakha hai
        for line in lines:
            add_glow_text(draw, line, W/2, y_text, font_med, "white", "black")
            y_text += int(H*0.06)

        # Meaning (Gold)
        lines_mean = textwrap.wrap(data['mean'], width=30)
        y_mean = y_text + 30
        for line in lines_mean:
            add_glow_text(draw, line, W/2, y_mean, font_small, "#FCEeb5", "black")
            y_mean += int(H*0.04)

        # Footer
        add_glow_text(draw, "350th Martyrdom Year | Guru Tegh Bahadur Ji", W/2, H*0.92, font_small, "#FFD700", "black")
        add_glow_text(draw, "Dev: Karan (Chitkara Univ)", W/2, H*0.96, font_small, "#888888", "black")

        return img
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- 4. UI ---
st.markdown("<h1 style='text-align: center;'>✨ NADAR ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #aaaaaa;'>Receive Your Personal Blessing</p>", unsafe_allow_html=True)

name_input = st.text_input("Enter Name:", placeholder="E.g. Karan")

if st.button("🌹 Get My Blessing 🌹", use_container_width=True):
    if name_input:
        sel = random.choice(saloks_data)
        img = create_poster(name_input, sel)
        
        if img:
            st.image(img, use_column_width=True)
            # Download Logic
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=100)
            st.download_button("📥 Download HD Poster", data=buf.getvalue(), file_name="Nadar.jpg", mime="image/jpeg", use_container_width=True)
    else:
        st.warning("Naam likho veerji!")