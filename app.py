import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import io
import textwrap
import requests
from streamlit_lottie import st_lottie

# --- 1. PRO CONFIG & ASSETS ---
st.set_page_config(page_title="Nadar: The 9th Light", page_icon="🕯️", layout="centered")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Live Diya Animation (Internet se chalega)
lottie_diya = load_lottieurl("https://lottie.host/6b696006-2037-4606-a746-6d7422600a02/Xz2w8qK2Qo.json")

# --- 2. MODERN UI/UX (GLASSMORPHISM STYLE) ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #1a1a1a 0%, #000000 100%);
        color: #FFD700;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        font-family: 'serif';
        text-shadow: 0px 0px 20px #FFD700;
        font-size: 3.5rem !important;
    }
    /* Glass Effect Input */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1);
        color: #FFD700;
        text-align: center;
        border: 1px solid #FFD700;
        border-radius: 15px;
        font-size: 20px;
        padding: 10px;
    }
    /* Glowing Button */
    .stButton>button {
        background: linear-gradient(90deg, #8E6E12, #F2D692, #8E6E12);
        color: black;
        font-weight: 900;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0px 0px 25px rgba(255, 215, 0, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 40px rgba(255, 215, 0, 0.7);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FULL SHABADS DATABASE (Longer & Deeper) ---
saloks_data = [
    {
        "text": "Gun gobind gaiyo nahi, janam akarth keen.\nKahu nanak bhaj har mana, jih bidh jal kau meen.\nBikhian sio kahe rachio, nimakh na hohi udas.\nKahu nanak bhaj har mana, pare na jam ki faas.",
        "mean": "You have not sung the Lord's praises; your life is rendering useless. Says Nanak, worship the Lord, just as the fish loves the water. Why are you engrossed in sin? Worship the Lord, and the noose of death shall not catch you."
    },
    {
        "text": "Jo upjio so binas hai, paro aaj ke kaal.\nNanak har gun gai le, chaad sagal janjal.\nDohra: Bal chutkyo bandhan pare, kachu na hot upaaye.\nKahu nanak ab ot har, gaj jio hohu sahaaye.",
        "mean": "Whatever is created shall be destroyed; understand this today. O Nanak, sing the Glorious Praises of the Lord, and give up all other entanglements. Strength is gone, bonds are shackles. Says Nanak, the Lord is now my Support; He helps me as He helped the elephant."
    },
    {
        "text": "Jagat bhikhari phirat hai, sab ko data ram.\nKahu nanak man simar tih, puran hove kaam.\nJih prani haumai taji, karta ram pachaan.\nKahu nanak voh mukt nar, ih man saachi maan.",
        "mean": "The whole world begs, but the One Lord is the Giver of all. Says Nanak, meditate on Him in your mind, and your affairs shall be resolved. That mortal who renounces ego, realizes the Creator. Says Nanak, that man is liberated; accept this as the Truth."
    },
    {
        "text": "Chetna hai tau chet lai, nis din mai prani.\nChin chin audh bihaat hai, phoote ghat jio pani.\nHar gun kahte kahan daray, jih charo akal.\nNanak man re simar le, beetay avadh nidan.",
        "mean": "If you are to be conscious, then be conscious of Him, night and day, O mortal. Moment by moment, your life is running out, like water from a cracked pitcher. Why do you hesitate to sing the Lord's Praises? O Nanak, meditate on Him in your mind; your life is coming to its end."
    },
    {
        "text": "Sukh dukh jih parsai nahi, lobh moh abhiman.\nKahu nanak sun re mana, so murat bhagwan.\nUstat ninda dou tiagai, khojai pad nirbana.\nJan nanak ih khel kathin hai, kou gurmukh jana.",
        "mean": "One who is not touched by pleasure or pain, greed, attachment, or pride—says Nanak, listen, O mind: he is the very image of God. One who renounces both praise and slander, and seeks the supreme state of Nirvana—O servant Nanak, this is such a difficult game; only a few Gurmukhs understand it."
    }
]

# --- 4. PRO IMAGE ENGINE ---
def get_fitted_font(draw, text, font_path, max_width, max_font_size):
    size = max_font_size
    try:
        font = ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()
    
    while draw.textbbox((0, 0), text, font=font)[2] > max_width and size > 15:
        size -= 2
        font = ImageFont.truetype(font_path, size)
    return font

def create_poster(name, data):
    try:
        img = Image.open("background.jpg").convert("RGBA") # Changed to RGBA for Transparency logic
        
        # Darken Image
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.5)
        
        W, H = img.size
        draw = ImageDraw.Draw(img)

        # --- STICKER LOGIC (DIYA) ---
        try:
            diya_sticker = Image.open("diya.png").convert("RGBA")
            # Resize Diya (15% of poster width)
            diya_w = int(W * 0.25)
            aspect_ratio = diya_sticker.height / diya_sticker.width
            diya_h = int(diya_w * aspect_ratio)
            diya_sticker = diya_sticker.resize((diya_w, diya_h))
            
            # Paste Diya at Top Center
            diya_x = (W - diya_w) // 2
            diya_y = int(H * 0.05)
            img.paste(diya_sticker, (diya_x, diya_y), diya_sticker)
        except:
            pass # Agar diya.png nahi mili to crash mat hona

        # --- TEXT RENDERING ---
        font_path = "font.ttf"
        
        # 1. Name (Below Diya)
        name_font = get_fitted_font(draw, name.upper(), font_path, W*0.8, int(H*0.07))
        draw.text((W/2, H*0.18), name.upper(), font=name_font, fill="#FFD700", anchor="mm", stroke_width=2, stroke_fill="black")
        
        # 2. "Received the Nadar"
        small_font = ImageFont.truetype(font_path, int(H*0.02))
        draw.text((W/2, H*0.24), "RECEIVED THE 9TH LIGHT:", font=small_font, fill="#AAAAAA", anchor="mm")

        # 3. FULL SHABAD (Multiline Logic)
        salok_font = ImageFont.truetype(font_path, int(H*0.035)) # Smaller font for long text
        lines = textwrap.wrap(data['text'], width=35) # Wider wrap for stanzas
        
        y_text = H * 0.38
        for line in lines:
            # Black Glow behind text for readability
            for off in [-2, -1, 1, 2]:
                draw.text((W/2+off, y_text), line, font=salok_font, fill="black", anchor="mm")
                draw.text((W/2, y_text+off), line, font=salok_font, fill="black", anchor="mm")
            
            draw.text((W/2, y_text), line, font=salok_font, fill="#FFFFFF", anchor="mm")
            y_text += int(H*0.05) # Spacing

        # 4. MEANING (Italic style)
        mean_font = ImageFont.truetype(font_path, int(H*0.022))
        lines_mean = textwrap.wrap(data['mean'], width=45)
        y_mean = y_text + 30
        for line in lines_mean:
            draw.text((W/2, y_mean), line, font=mean_font, fill="#F2D692", anchor="mm", stroke_width=1, stroke_fill="black")
            y_mean += int(H*0.035)

        # 5. FOOTER
        draw.text((W/2, H*0.92), "350TH MARTYRDOM YEAR | GURU TEGH BAHADUR JI", font=small_font, fill="#FFD700", anchor="mm")
        draw.text((W/2, H*0.95), "DEV: KARAN (CHITKARA UNIV)", font=small_font, fill="#888888", anchor="mm")

        return img.convert("RGB") # Convert back to JPG compatible
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- 5. FRONTEND DISPLAY ---

# Lottie Animation (Live Diya)
if lottie_diya:
    st_lottie(lottie_diya, height=150, key="diya")

st.markdown("<h1 style='text-align: center; margin-top: -20px;'>✨ NADAR ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888;'>Enter your name to receive a Complete Shabad</p>", unsafe_allow_html=True)

name_input = st.text_input(" ", placeholder="YOUR NAME (e.g. KARAN SINGH)")

if st.button("🌹 REVEAL MY BLESSING 🌹", use_container_width=True):
    if name_input:
        sel = random.choice(saloks_data)
        img = create_poster(name_input, sel)
        
        if img:
            st.image(img, use_column_width=True)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=95)
            st.download_button("📥 DOWNLOAD POSTER", data=buf.getvalue(), file_name="Nadar_Shabad.jpg", mime="image/jpeg", use_container_width=True)
    else:
        st.warning("Please enter your name.")