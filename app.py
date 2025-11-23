import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import io
import textwrap

# --- APP CONFIG ---
st.set_page_config(page_title="Nadar: The 9th Light", page_icon="🕯️", layout="centered")

# --- DATA ---
saloks_data = [
    {"text": "Chinta ta ki kijiye, jo anhoni hoye.", "mean": "Worry only about what is not destined to happen."},
    {"text": "Bhai kahu kau det neh, neh bhai manat aan.", "mean": "Fear none, and frighten none."},
    {"text": "Gun gobind gaiyo nahi, janam akarth keen.", "mean": "You have not sung His praises; life is slipping away."},
    {"text": "Jo upjio so binas hai, paro aaj ke kaal.", "mean": "Whatever is created shall be destroyed; understand this today."},
    {"text": "Bal chutkyo bandhan pare, kachu na hot upaaye.", "mean": "Strength is gone, but surrender to Him saves you."},
    {"text": "Sang sakha sab taj gaye, kou na nibhyo saath.", "mean": "Friends left; only the Divine remains with you."},
    {"text": "Patit udharan bhay haran, sukh sagar narayan.", "mean": "He is the Destroyer of fear, the Ocean of Peace."},
    {"text": "Jagat bhikhari phirat hai, sab ko data ram.", "mean": "The world begs, but the One Lord gives to all."},
    {"text": "Ram simar ram simar, ihai tero kaaj hai.", "mean": "Remember the Lord; this is your only true work."},
    {"text": "Seva karat hoye nihkame.", "mean": "Serve without desire, and attain the Lord."},
]

# --- DESIGNER LOGIC (WITH GLOW EFFECT) ---
def draw_text_with_stroke(draw, text, x, y, font, text_color, stroke_color, stroke_width):
    # Pehle Black Border (Stroke) banao
    draw.text((x, y), text, font=font, fill=text_color, anchor="mm", stroke_width=stroke_width, stroke_fill=stroke_color)

def create_poster(name, data):
    try:
        img = Image.open("background.jpg")
        W, H = img.size
        draw = ImageDraw.Draw(img)

        # --- LOAD FONTS (BIGGER SIZE) ---
        try:
            # Sizes ab bohot bade kar diye hain
            font_name = ImageFont.truetype("font.ttf", int(H*0.08))  # Naam Bada
            font_text = ImageFont.truetype("font.ttf", int(H*0.05))  # Salok Bada
            font_mean = ImageFont.truetype("font.ttf", int(H*0.03))  # Meaning Normal
            font_small = ImageFont.truetype("font.ttf", int(H*0.025)) # Footer
        except:
            # Agar font nahi mila toh error dikhao (taki pata chale)
            st.error("⚠️ Font File Missing! Please put 'font.ttf' in the folder.")
            font_name = ImageFont.load_default()
            font_text = ImageFont.load_default()
            font_mean = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # --- 1. NAME (GOLDEN WITH BLACK OUTLINE) ---
        # Naam thoda neeche kiya taki kate na
        draw_text_with_stroke(draw, name.upper(), W/2, H*0.22, font_name, "#FFD700", "#000000", 4)
        
        # Subtitle
        draw.text((W/2, H*0.28), "receives the Nadar:", font=font_mean, fill="#DDDDDD", anchor="mm")

        # --- 2. SALOK (WHITE GLOWING) ---
        lines = textwrap.wrap(data['text'], width=20) # Choti width taki lines break hon
        y_text = H * 0.42 # Thoda upar shift kiya
        
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_text)
            line_height = bbox[3] - bbox[1]
            # White text with Black Shadow
            draw_text_with_stroke(draw, line, W/2, y_text, font_text, "#FFFFFF", "#000000", 3)
            y_text += line_height + 30 # Gap

        # --- 3. MEANING (LIGHT GOLD) ---
        lines_mean = textwrap.wrap(data['mean'], width=35)
        y_mean = y_text + 40
        for line in lines_mean:
            bbox = draw.textbbox((0, 0), line, font=font_mean)
            line_height = bbox[3] - bbox[1]
            draw_text_with_stroke(draw, line, W/2, y_mean, font_mean, "#FCEeb5", "#000000", 2)
            y_mean += line_height + 20

        # --- 4. FOOTER ---
        draw.text((W/2, H*0.90), "Guru Tegh Bahadur Ji | 350th Year", font=font_small, fill="#FFD700", anchor="mm")
        draw.text((W/2, H*0.94), "Sis Ganj Sahib • Anandpur Sahib", font=font_small, fill="#FFFFFF", anchor="mm")
        
        # Watermark
        draw.text((W/2, H*0.97), "Dev: Karan (Chitkara Univ)", font=font_small, fill="#888888", anchor="mm")

        return img
    except Exception as e:
        st.error(f"Image Error: {e}")
        return None

# --- UI ---
st.markdown("<h1 style='text-align: center; color: #FFD700;'>✨ NADAR ✨</h1>", unsafe_allow_html=True)
name_input = st.text_input("Enter Name:", placeholder="Example: Karan")

if st.button("🌹 Receive My Blessing 🌹", use_container_width=True):
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
