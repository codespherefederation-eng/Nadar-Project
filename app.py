import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import io
import textwrap
import requests
from streamlit_lottie import st_lottie

# --- 1. PRO CONFIG & ASSETS ---
st.set_page_config(page_title="Nadar: The 9th Light", page_icon="🕯️", layout="centered")

# Load Live Animation (Diya) directly from Internet
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Lottie Animation URL (Golden Diya)
lottie_diya = load_lottieurl("https://lottie.host/4b505036-6533-4d47-a692-577726622606/p1Fz5Xy8K6.json")

# --- 2. MODERN UI (Glassmorphism) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #FFD700;
    }
    /* Title Glow */
    h1 {
        font-family: 'serif';
        text-align: center;
        color: #FFD700;
        text-shadow: 0px 0px 20px #FFD700;
        font-size: 3rem !important;
    }
    /* Input Field Styling */
    .stTextInput>div>div>input {
        background-color: #111;
        color: #FFD700;
        text-align: center;
        border: 1px solid #FFD700;
        border-radius: 10px;
        font-size: 18px;
    }
    /* Golden Button */
    .stButton>button {
        background: linear-gradient(90deg, #8E6E12 0%, #F2D692 50%, #8E6E12 100%);
        color: black;
        font-weight: 900;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0px 0px 30px rgba(255, 215, 0, 0.3);
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LONG SHABAD DATABASE (Full Teachings) ---
saloks_data = [
    {
        "text": "Gun gobind gaiyo nahi, janam akarth keen.\nKahu nanak bhaj har mana, jih bidh jal kau meen.\nBikhian sio kahe rachio, nimakh na hohi udas.\nKahu nanak bhaj har mana, pare na jam ki faas.",
        "mean": "You have not sung the Lord's praises; your life is wasted. Says Nanak, worship the Lord, just as the fish loves the water. Why are you engrossed in sin? Worship the Lord, and the noose of death shall not catch you."
    },
    {
        "text": "Jo upjio so binas hai, paro aaj ke kaal.\nNanak har gun gai le, chaad sagal janjal.\nDohra: Bal chutkyo bandhan pare, kachu na hot upaaye.\nKahu nanak ab ot har, gaj jio hohu sahaaye.",
        "mean": "Whatever is created shall be destroyed; understand this today. O Nanak, sing the Glorious Praises of the Lord, and give up all other entanglements. Strength is gone, bonds are shackles. Says Nanak, the Lord is now my Support."
    },
    {
        "text": "Jagat bhikhari phirat hai, sab ko data ram.\nKahu nanak man simar tih, puran hove kaam.\nJih prani haumai taji, karta ram pachaan.\nKahu nanak voh mukt nar, ih man saachi maan.",
        "mean": "The whole world begs, but the One Lord is the Giver of all. Says Nanak, meditate on Him in your mind, and your affairs shall be resolved. That mortal who renounces ego, realizes the Creator."
    },
    {
        "text": "Chetna hai tau chet lai, nis din mai prani.\nChin chin audh bihaat hai, phoote ghat jio pani.\nHar gun kahte kahan daray, jih charo akal.\nNanak man re simar le, beetay avadh nidan.",
        "mean": "If you are to be conscious, then be conscious of Him. Moment by moment, your life is running out, like water from a cracked pitcher. Why do you hesitate to sing the Lord's Praises? O Nanak, meditate on Him."
    },
    {
        "text": "Sukh dukh jih parsai nahi, lobh moh abhiman.\nKahu nanak sun re mana, so murat bhagwan.\nUstat ninda dou tiagai, khojai pad nirbana.\nJan nanak ih khel kathin hai, kou gurmukh jana.",
        "mean": "One who is not touched by pleasure or pain, greed, attachment, or pride—says Nanak, listen, O mind: he is the very image of God. One who renounces both praise and slander, and seeks the supreme state of Nirvana."
    }
]

# --- 4. SMART IMAGE ENGINE (The Fix) ---

def draw_text_with_glow(draw, text, x, y, font, text_color, glow_color="black"):
    """Draws text with a strong shadow/glow for readability"""
    # Thick Stroke (Outline)
    for off in [-2, -1, 1, 2]:
        draw.text((x+off, y), text, font=font, fill=glow_color, anchor="mm")
        draw.text((x, y+off), text, font=font, fill=glow_color, anchor="mm")
    draw.text((x, y), text, font=font, fill=text_color, anchor="mm")

def create_poster(name, data):
    try:
        img = Image.open("background.jpg").convert("RGBA")
        
        # Darken Background (Taaki text chamke)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.4) # 60% Darker
        
        W, H = img.size
        draw = ImageDraw.Draw(img)

        font_path = "font.ttf"

        # --- A. DIYA STICKER (Top) ---
        current_y = int(H * 0.05) # Start from 5% top
        try:
            diya = Image.open("diya.png").convert("RGBA")
            # Resize Diya (18% of width)
            diya_w = int(W * 0.18)
            aspect = diya.height / diya.width
            diya_h = int(diya_w * aspect)
            diya = diya.resize((diya_w, diya_h))
            
            # Paste Centered
            diya_x = (W - diya_w) // 2
            img.paste(diya, (diya_x, current_y), diya)
            current_y += diya_h + 30 # Move Y down
        except:
            pass # Agar Diya nahi mila to skip karo

        # --- B. NAME (Below Diya) ---
        # Smart Font Sizing for Name
        name_size = int(H * 0.07)
        try:
            name_font = ImageFont.truetype(font_path, name_size)
        except:
            name_font = ImageFont.load_default()
            
        draw_text_with_glow(draw, name.upper(), W/2, current_y, name_font, "#FFD700")
        current_y += int(H * 0.05)

        # --- C. SUBTITLE ---
        try:
            sub_font = ImageFont.truetype(font_path, int(H * 0.02))
        except:
            sub_font = ImageFont.load_default()
            
        draw_text_with_glow(draw, "RECEIVED THE 9TH LIGHT:", W/2, current_y, sub_font, "#CCCCCC")
        current_y += int(H * 0.08) # Gap before Shabad

        # --- D. LONG SHABAD (The Hard Part) ---
        # Hum font size fix rakhenge, lekin wrapping adjust karenge
        shabad_font_size = int(H * 0.035) # Thoda chhota font taaki lamba text aa sake
        try:
            shabad_font = ImageFont.truetype(font_path, shabad_font_size)
        except:
            shabad_font = ImageFont.load_default()

        # Text Wrapping (35 characters per line)
        lines = textwrap.wrap(data['text'], width=30)
        
        for line in lines:
            draw_text_with_glow(draw, line, W/2, current_y, shabad_font, "#FFFFFF")
            current_y += int(H * 0.045) # Line Height

        current_y += 30 # Gap for Meaning

        # --- E. MEANING (Bottom Section) ---
        mean_font_size = int(H * 0.022)
        try:
            mean_font = ImageFont.truetype(font_path, mean_font_size)
        except:
            mean_font = ImageFont.load_default()
            
        lines_mean = textwrap.wrap(data['mean'], width=45)
        for line in lines_mean:
            draw_text_with_glow(draw, line, W/2, current_y, mean_font, "#FCEEB5")
            current_y += int(H * 0.03)

        # --- F. FOOTER & BORDER ---
        # Footer fixed at bottom
        try:
            foot_font = ImageFont.truetype(font_path, int(H * 0.025))
        except:
            foot_font = ImageFont.load_default()
            
        draw_text_with_glow(draw, "350TH MARTYRDOM YEAR | GURU TEGH BAHADUR JI", W/2, H*0.92, foot_font, "#FFD700")
        draw_text_with_glow(draw, "DEV: KARAN (CHITKARA UNIV)", W/2, H*0.95, foot_font, "#888888")

        # Golden Border
        border = 20
        draw.rectangle([border, border, W-border, H-border], outline="#FFD700", width=6)

        return img.convert("RGB")
    except Exception as e:
        st.error(f"Image Error: {e}")
        return None

# --- 5. UI FRONTEND ---

# LIVE ANIMATION (Diya on Site)
if lottie_diya:
    st_lottie(lottie_diya, height=180, key="diya_anim")

st.markdown("<h1 style='margin-top: -20px;'>✨ NADAR ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #AAAAAA; margin-bottom: 30px;'>Enter your name to receive a Complete Shabad</p>", unsafe_allow_html=True)

name_input = st.text_input(" ", placeholder="YOUR NAME (E.g. KARAN)")

if st.button("🌹 REVEAL MY BLESSING 🌹", use_container_width=True):
    if name_input:
        with st.spinner("Seeking blessings..."):
            sel = random.choice(saloks_data)
            img = create_poster(name_input, sel)
            
            if img:
                st.image(img, use_column_width=True)
                
                # Download Button
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=95)
                st.download_button("📥 DOWNLOAD HD POSTER", data=buf.getvalue(), file_name="Nadar_Blessing.jpg", mime="image/jpeg", use_container_width=True)
                st.balloons()
    else:
        st.warning("Please enter your name first.")