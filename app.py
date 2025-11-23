import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import io
import textwrap
import requests
from streamlit_lottie import st_lottie

# --- 1. APP CONFIGURATION (Dark & Royal) ---
st.set_page_config(page_title="Nadar: The 9th Light", page_icon="🕯️", layout="centered")

# Custom CSS for UI
st.markdown("""
    <style>
    .stApp {
        background-color: #050505;
        color: #FFD700;
    }
    h1 {
        font-family: 'serif';
        text-align: center;
        color: #FFD700;
        text-shadow: 0px 0px 15px #FFD700;
    }
    .stButton>button {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 50px;
        padding: 15px 30px;
        font-size: 18px;
        width: 100%;
        box-shadow: 0px 0px 20px rgba(255, 215, 0, 0.5);
    }
    .stTextInput>div>div>input {
        text-align: center;
        background-color: #111;
        border: 2px solid #FFD700;
        color: #FFD700;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE WISDOM DATABASE (Full Shabads) ---
saloks_data = [
    {
        "text": "Chinta ta ki kijiye, jo anhoni hoye.\nIh marag sansar ko, nanak thir nahi koye.",
        "mean": "Worry only about what is not destined to happen. In this path of the world, O Nanak, nothing is permanent."
    },
    {
        "text": "Bhai kahu kau det neh, neh bhai manat aan.\nKahu nanak sun re mana, giani tahi bakhan.",
        "mean": "One who fears none, and frightens none - says Nanak, listen O mind, call him truly wise."
    },
    {
        "text": "Gun gobind gaiyo nahi, janam akarth keen.\nKahu nanak bhaj har mana, jih bidh jal kau meen.",
        "mean": "You have not sung the Lord's praises; your life is rendering useless. Worship the Lord, just as the fish loves the water."
    },
    {
        "text": "Jo upjio so binas hai, paro aaj ke kaal.\nNanak har gun gai le, chaad sagal janjal.",
        "mean": "Whatever is created shall be destroyed; understand this today. O Nanak, sing the Glorious Praises of the Lord, and give up all other entanglements."
    },
    {
        "text": "Bal chutkyo bandhan pare, kachu na hot upaaye.\nKahu nanak ab ot har, gaj jio hohu sahaaye.",
        "mean": "Strength is gone, bonds are shackles. Says Nanak, the Lord is now my Support; He helps me as He helped the elephant."
    },
    {
        "text": "Sang sakha sab taj gaye, kou na nibhyo saath.\nKahu nanak ih bipat mai, tek ek raghunath.",
        "mean": "Friends and companions have all left; no one remains with you. Says Nanak, in this calamity, the Lord is your only Support."
    },
    {
        "text": "Sukh dukh jih parsai nahi, lobh moh abhiman.\nKahu nanak sun re mana, so murat bhagwan.",
        "mean": "One who is not touched by pleasure or pain, greed, attachment, or pride—says Nanak, listen O mind, he is the very image of God."
    }
]

# --- 3. IMAGE PROCESSING ENGINE ---

def get_fitted_font(draw, text, font_path, max_width, max_font_size):
    """ Auto-resize font so name doesn't cut off """
    size = max_font_size
    try:
        font = ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()
    
    while draw.textbbox((0, 0), text, font=font)[2] > max_width and size > 20:
        size -= 2
        font = ImageFont.truetype(font_path, size)
    return font

def draw_text_with_stroke(draw, text, x, y, font, text_color, stroke_color="black", stroke_width=2):
    """ Adds a black outline to text so it is readable on any background """
    draw.text((x, y), text, font=font, fill=text_color, anchor="mm", stroke_width=stroke_width, stroke_fill=stroke_color)

def create_poster(name, data):
    try:
        # 1. Load Background
        img = Image.open("background.jpg").convert("RGBA")
        
        # Darken Background (Taaki text chamke)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.5) 
        
        W, H = img.size
        draw = ImageDraw.Draw(img)

        # --- 2. ASSETS SETUP ---
        font_path = "font.ttf"
        
        # --- 3. DIYA STICKER (Top Center) ---
        try:
            diya = Image.open("diya.png").convert("RGBA")
            # Resize Diya to 20% of width
            diya_w = int(W * 0.20)
            aspect = diya.height / diya.width
            diya_h = int(diya_w * aspect)
            diya = diya.resize((diya_w, diya_h))
            
            # Paste Diya (Top padding 5%)
            diya_x = (W - diya_w) // 2
            diya_y = int(H * 0.05)
            img.paste(diya, (diya_x, diya_y), diya)
            
            # Set Next Y position below Diya
            current_y = diya_y + diya_h + 20
        except:
            current_y = int(H * 0.15) # Agar diya nahi mila to default position

        # --- 4. NAME (Below Diya) ---
        name_font = get_fitted_font(draw, name.upper(), font_path, W*0.8, int(H*0.08))
        draw_text_with_stroke(draw, name.upper(), W/2, current_y, name_font, "#FFD700", "black", 3)
        
        current_y += int(H * 0.06) # Gap

        # --- 5. SUBTITLE ---
        small_font = ImageFont.truetype(font_path, int(H*0.02))
        draw_text_with_stroke(draw, "RECEIVED THE 9TH LIGHT:", W/2, current_y, small_font, "#DDDDDD", "black", 1)
        
        current_y += int(H * 0.08) # Bigger Gap for Shabad

        # --- 6. SHABAD (Center) ---
        # Wrap text (30 characters per line)
        lines = textwrap.wrap(data['text'], width=30)
        shabad_font = ImageFont.truetype(font_path, int(H*0.04))
        
        for line in lines:
            draw_text_with_stroke(draw, line, W/2, current_y, shabad_font, "#FFFFFF", "black", 3)
            current_y += int(H * 0.055) # Line height

        current_y += 20 # Gap

        # --- 7. MEANING (Below Shabad) ---
        mean_font = ImageFont.truetype(font_path, int(H*0.025))
        lines_mean = textwrap.wrap(data['mean'], width=40)
        
        for line in lines_mean:
            draw_text_with_stroke(draw, line, W/2, current_y, mean_font, "#FCEEB5", "black", 2)
            current_y += int(H * 0.04)

        # --- 8. FOOTER & BORDER ---
        # Footer Text
        draw_text_with_stroke(draw, "350TH MARTYRDOM YEAR | GURU TEGH BAHADUR JI", W/2, H*0.92, small_font, "#FFD700", "black", 2)
        draw_text_with_stroke(draw, "DEV: KARAN (CHITKARA UNIV)", W/2, H*0.95, small_font, "#888888", "black", 1)

        # Gold Border (Frame)
        border = 20
        draw.rectangle([border, border, W-border, H-border], outline="#FFD700", width=8)

        return img.convert("RGB") # Save karne ke liye wapas RGB
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None

# --- 4. UI FRONTEND ---
st.markdown("<h1 style='margin-bottom: -10px;'>✨ NADAR ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888;'>The 9th Light: Personalized Wisdom</p>", unsafe_allow_html=True)

# Live Animation (Diya)
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

lottie_diya = load_lottieurl("https://lottie.host/6b696006-2037-4606-a746-6d7422600a02/Xz2w8qK2Qo.json")
if lottie_diya:
    st_lottie(lottie_diya, height=120, key="diya")

# Input
name_input = st.text_input(" ", placeholder="YOUR NAME (E.g. KARAN)")

# Button
if st.button("🌹 REVEAL MY BLESSING 🌹", use_container_width=True):
    if name_input:
        with st.spinner("Connecting to History..."):
            sel = random.choice(saloks_data)
            img = create_poster(name_input, sel)
            
            if img:
                st.image(img, use_column_width=True)
                
                # Download
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=100)
                st.download_button("📥 DOWNLOAD HD POSTER", data=buf.getvalue(), file_name=f"Nadar_{name_input}.jpg", mime="image/jpeg", use_container_width=True)
                st.balloons()
    else:
        st.warning("Please enter your name first.")