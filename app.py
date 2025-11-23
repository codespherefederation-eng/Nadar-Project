import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import io
import textwrap

# --- 1. SETUP ---
st.set_page_config(page_title="Nadar: The 9th Light", page_icon="🕯️", layout="centered")

# Dark & Gold Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFD700; }
    .stButton>button {
        background: linear-gradient(45deg, #FFD700, #FFC107);
        color: black; font-weight: bold; border: none; padding: 10px 20px;
    }
    .stTextInput>div>div>input { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATABASE ---
saloks_data = [
    {"text": "Chinta ta ki kijiye, jo anhoni hoye.", "mean": "Worry only about what is not destined to happen."},
    {"text": "Bhai kahu kau det neh, neh bhai manat aan.", "mean": "Fear none, and frighten none."},
    {"text": "Gun gobind gaiyo nahi, janam akarth keen.", "mean": "You have not sung His praises; life is wasted."},
    {"text": "Jo upjio so binas hai, paro aaj ke kaal.", "mean": "Whatever is created shall be destroyed; understand this."},
    {"text": "Bal chutkyo bandhan pare, kachu na hot upaaye.", "mean": "Strength is gone, but surrender to Him saves you."},
    {"text": "Sang sakha sab taj gaye, kou na nibhyo saath.", "mean": "Friends have left; only the Divine remains with you."},
    {"text": "Patit udharan bhay haran, sukh sagar narayan.", "mean": "He is the Destroyer of fear, the Ocean of Peace."},
    {"text": "Ram simar ram simar, ihai tero kaaj hai.", "mean": "Remember the Lord; this is your only true work."},
]

# --- 3. DESIGN ENGINE (WITH SHADOWS) ---
def draw_text_with_shadow(draw, text, position, font, text_color="white", shadow_color="black", stroke_width=3):
    x, y = position
    # Draw Outline/Shadow first (Black)
    draw.text((x, y), text, font=font, fill=shadow_color, anchor="mm", stroke_width=stroke_width, stroke_fill=shadow_color)
    # Draw Main Text (Gold/White)
    draw.text((x, y), text, font=font, fill=text_color, anchor="mm")

def create_poster(name, data):
    try:
        img = Image.open("background.jpg")
        W, H = img.size
        draw = ImageDraw.Draw(img)

        # --- DYNAMIC FONTS ---
        try:
            # Fonts size image ke hisaab se change honge
            font_name = ImageFont.truetype("font.ttf", int(H*0.08)) # Bada Naam
            font_text = ImageFont.truetype("font.ttf", int(H*0.045)) # Salok
            font_mean = ImageFont.truetype("font.ttf", int(H*0.03)) # Meaning
            font_small = ImageFont.truetype("font.ttf", int(H*0.025)) # Footer
        except:
            font_name = ImageFont.load_default()
            font_text = ImageFont.load_default()
            font_mean = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # --- DRAWING (Center Alignment Logic) ---
        
        # 1. NAME (Top - Gold with Black Stroke)
        draw_text_with_shadow(draw, name.upper(), (W/2, H*0.20), font_name, "#FFD700", "black", 5)
        
        # Subtext
        draw_text_with_shadow(draw, "received the Nadar:", (W/2, H*0.27), font_small, "#DDDDDD", "black", 2)

        # 2. SALOK (Middle - White Glowing)
        lines = textwrap.wrap(data['text'], width=20) # Text wrap
        y_text = H * 0.45
        for line in lines:
            draw_text_with_shadow(draw, line, (W/2, y_text), font_text, "#FFFFFF", "black", 4)
            y_text += int(H*0.06) # Gap between lines

        # 3. MEANING (Bottom - Light Gold)
        lines_mean = textwrap.wrap(data['mean'], width=35)
        y_mean = y_text + int(H*0.05)
        for line in lines_mean:
            draw_text_with_shadow(draw, line, (W/2, y_mean), font_mean, "#FCEeb5", "black", 3)
            y_mean += int(H*0.04)

        # 4. FOOTER (Branding)
        draw_text_with_shadow(draw, "Guru Tegh Bahadur Ji | 350th Year", (W/2, H*0.90), font_small, "#FFD700", "black", 2)
        draw_text_with_shadow(draw, "Sis Ganj Sahib • Anandpur Sahib", (W/2, H*0.93), font_small, "#FFFFFF", "black", 2)
        draw_text_with_shadow(draw, "Dev: Karan (Chitkara Univ)", (W/2, H*0.97), font_small, "#888888", "black", 1)

        return img
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- 4. UI ---
st.markdown("<h1 style='text-align: center;'>✨ NADAR ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>The 9th Light: Receive Your Blessing</p>", unsafe_allow_html=True)

name_input = st.text_input("Enter Name:", placeholder="E.g. Karan")

if st.button("🌹 Receive My Hukam 🌹", use_container_width=True):
    if name_input:
        sel = random.choice(saloks_data)
        img = create_poster(name_input, sel)
        
        if img:
            st.image(img, use_column_width=True)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=100)
            st.download_button("📥 Download Poster", data=buf.getvalue(), file_name="Nadar.jpg", mime="image/jpeg", use_container_width=True)
    else:
        st.warning("Naam likho veerji!")