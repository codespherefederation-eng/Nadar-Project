import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import io
import textwrap

# --- 1. APP CONFIG ---
st.set_page_config(page_title="Nadar: The 9th Light", page_icon="🕯️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #D4AF37; }
    .stButton>button {
        background: linear-gradient(to bottom, #D4AF37, #AA8E2D);
        color: black; font-weight: bold; border: none; padding: 12px 25px; border-radius: 5px;
        letter-spacing: 2px; text-transform: uppercase;
    }
    .stTextInput>div>div>input { 
        background-color: #1a1a1a; color: #D4AF37; text-align: center; border: 1px solid #D4AF37; 
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
    {"text": "Patit udharan bhay haran, sukh sagar narayan.", "mean": "He is the Destroyer of fear, Ocean of Peace."},
    {"text": "Ram simar ram simar, ihai tero kaaj hai.", "mean": "Remember the Lord; this is your only true work."},
]

# --- 3. SMART DESIGN ENGINE ---

def get_fitted_font(draw, text, font_path, max_width, max_font_size):
    """Yeh function text ko chhota karega agar wo zyada lamba hai"""
    size = max_font_size
    font = ImageFont.truetype(font_path, size)
    
    # Jab tak text width box se badi hai, size kam karte raho
    while draw.textbbox((0, 0), text, font=font)[2] > max_width and size > 20:
        size -= 2
        font = ImageFont.truetype(font_path, size)
    return font

def create_poster(name, data):
    try:
        # Load & Darken Image
        img = Image.open("background.jpg").convert("RGB")
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.6) # Thoda dark kiya taaki text pop kare
        
        W, H = img.size
        draw = ImageDraw.Draw(img, "RGBA") # RGBA for transparency

        # --- ADD GRADIENT OVERLAY (Netflix Style Shadow) ---
        # Text ke peeche ek halka kaala parda (Gradient) lagayenge taaki text padha jaye
        overlay = Image.new('RGBA', img.size, (0,0,0,0))
        overlay_draw = ImageDraw.Draw(overlay)
        # Top Gradient (Naam ke liye)
        overlay_draw.rectangle([(0, 0), (W, H*0.35)], fill=(0, 0, 0, 180)) 
        # Bottom Gradient (Meaning ke liye)
        overlay_draw.rectangle([(0, H*0.85), (W, H)], fill=(0, 0, 0, 200))
        
        img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(img)

        # --- SMART FONTS ---
        # Define Safe Area (Padding) - Side se 10% jagah chod kar
        safe_width = W * 0.85 
        
        try:
            font_path = "font.ttf"
            # Initial sizes (Maximum)
            name_font = get_fitted_font(draw, name.upper(), font_path, safe_width, int(H*0.09))
            salok_font = ImageFont.truetype(font_path, int(H*0.045))
            mean_font = ImageFont.truetype(font_path, int(H*0.025))
            small_font = ImageFont.truetype(font_path, int(H*0.02))
        except:
            st.error("Font file missing!")
            return None

        # --- ELEGANT TEXT DRAWING ---
        
        # 1. ROYAL BORDER (Patla aur Elegant)
        border_gap = 30
        draw.rectangle([border_gap, border_gap, W-border_gap, H-border_gap], outline="#D4AF37", width=5)
        # Inner thin line
        draw.rectangle([border_gap+10, border_gap+10, W-(border_gap+10), H-(border_gap+10)], outline="#D4AF37", width=1)

        # 2. NAME (Auto-Fitted, Premium Gold)
        # Ab ye katega nahi, size apne aap chhota ho jayega
        draw.text((W/2, H*0.15), name.upper(), font=name_font, fill="#D4AF37", anchor="mm")
        
        # 3. SUBTITLE (Elegant White)
        draw.text((W/2, H*0.23), "RECIEVED THE NADAR", font=small_font, fill="#AAAAAA", anchor="mm", spacing=10)

        # 4. SALOK (Clean White)
        lines = textwrap.wrap(data['text'], width=20)
        y_text = H * 0.42
        for line in lines:
            draw.text((W/2, y_text), line, font=salok_font, fill="#FFFFFF", anchor="mm")
            y_text += int(H*0.06)

        # 5. MEANING (Italic Feel - Light Gold)
        lines_mean = textwrap.wrap(data['mean'], width=35)
        y_mean = y_text + 40
        for line in lines_mean:
            draw.text((W/2, y_mean), line, font=mean_font, fill="#F2D692", anchor="mm")
            y_mean += int(H*0.04)

        # 6. FOOTER (Clean)
        draw.text((W/2, H*0.92), "350TH MARTYRDOM YEAR | GURU TEGH BAHADUR JI", font=small_font, fill="#D4AF37", anchor="mm")
        draw.text((W/2, H*0.95), "DEV: KARAN (CHITKARA UNIV)", font=small_font, fill="#666666", anchor="mm")

        return img
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- UI ---
st.markdown("<h1 style='text-align: center; letter-spacing: 3px; color: #D4AF37;'>✨ NADAR ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888; font-size: 12px;'>ENTER YOUR NAME FOR A DIVINE BLESSING</p>", unsafe_allow_html=True)

name_input = st.text_input(" ", placeholder="NAME (e.g. KARANDEEP SINGH)")

if st.button("REVEAL BLESSING", use_container_width=True):
    if name_input:
        sel = random.choice(saloks_data)
        img = create_poster(name_input, sel)
        if img:
            st.image(img, use_column_width=True)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=95)
            st.download_button("DOWNLOAD POSTER", data=buf.getvalue(), file_name="Nadar.jpg", mime="image/jpeg", use_container_width=True)
    else:
        st.warning("Please enter your name.")