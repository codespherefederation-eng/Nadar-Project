import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import io
import textwrap

# --- 1. APP CONFIGURATION (Royal & Cinematic) ---
st.set_page_config(page_title="Nadar: The 9th Light", page_icon="🕯️", layout="centered")

# Custom CSS for that "Outstanding" Dark & Gold Look
st.markdown("""
    <style>
    .stApp {
        background-color: #050505;
        color: #FFD700;
    }
    h1 {
        color: #FFD700 !important;
        text-align: center;
        font-family: 'serif';
        font-weight: 700;
        text-shadow: 0px 0px 10px #FFD700; /* Glowing Text Effect */
    }
    h3 {
        font-family: 'sans-serif';
        font-weight: 300;
        letter-spacing: 2px;
    }
    .stButton>button {
        color: #000000;
        background: linear-gradient(to right, #FFD700, #FDB931); /* Gold Gradient Button */
        border: none;
        border-radius: 30px;
        font-size: 20px;
        font-weight: bold;
        padding: 15px 30px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 15px #FFD700;
    }
    .stTextInput>div>div>input {
        background-color: #1E1E1E;
        color: white;
        border: 1px solid #FFD700;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GURU TEGH BAHADUR JI'S WISDOM (DATABASE) ---
saloks_data = [
    {"text": "Chinta ta ki kijiye, jo anhoni hoye.", "mean": "Worry only about what is not destined to happen. What is destined, will happen."},
    {"text": "Bhai kahu kau det neh, neh bhai manat aan.", "mean": "One who fears none, and frightens none, is truly wise."},
    {"text": "Gun gobind gaiyo nahi, janam akarth keen.", "mean": "You have not sung the Lord's praises; your life is slipping away in vain."},
    {"text": "Jo upjio so binas hai, paro aaj ke kaal.", "mean": "Whatever is created shall be destroyed; understand this reality today."},
    {"text": "Bal chutkyo bandhan pare, kachu na hot upaaye.", "mean": "Strength is gone, bonds are shackles. But when you surrender, He saves you."},
    {"text": "Sang sakha sab taj gaye, kou na nibhyo saath.", "mean": "Friends and companions have all left; only the Divine remains with you."},
    {"text": "Patit udharan bhay haran, sukh sagar narayan.", "mean": "He is the Saver of sinners, the Destroyer of fear, the Ocean of Peace."},
    {"text": "Jagat bhikhari phirat hai, sab ko data ram.", "mean": "The whole world begs, but the One Lord is the Giver of all."},
    {"text": "Sukh dukh jih parsai nahi, lobh moh abhiman.", "mean": "One who is not touched by pleasure or pain, greed, attachment, or pride—is the image of God."},
    {"text": "Ghat ghat mai har ju basai, santan kahiyo pukar.", "mean": "The Lord abides in every heart; the Saints proclaim this truth aloud."},
    {"text": "Ram simar ram simar, ihai tero kaaj hai.", "mean": "Remember the Lord, remember the Lord; this is your only true work."},
    {"text": "Jih prani haumai taji, karta ram pachaan.", "mean": "That mortal who renounces ego, realizes the Creator."},
    {"text": "Seva karat hoye nihkame.", "mean": "Serve without the desire for reward, and you shall attain the Lord."},
    {"text": "Prani kaun upay kare.", "mean": "O mortal, what efforts should you make to attain the Lord's love?"},
    {"text": "Man re kaun kumat tai leeni.", "mean": "O mind, what evil counsel have you accepted?"},
]

# --- 3. IMAGE GENERATION ENGINE ---
def create_poster(name, data):
    try:
        # Load Background (Sis Ganj Sahib Image)
        img = Image.open("background.jpg")
        draw = ImageDraw.Draw(img)
        W, H = img.size

        # Load Fonts
        try:
            # Dynamic Font Sizing based on Image Height
            font_name = ImageFont.truetype("font.ttf", int(H*0.07)) 
            font_text = ImageFont.truetype("font.ttf", int(H*0.045))
            font_mean = ImageFont.truetype("font.ttf", int(H*0.028))
            font_small = ImageFont.truetype("font.ttf", int(H*0.022))
        except:
            font_name = ImageFont.load_default()
            font_text = ImageFont.load_default()
            font_mean = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # -- DESIGN LOGIC --
        
        # 1. Name (Top Center - Golden)
        draw.text((W/2, H*0.20), f"{name}", font=font_name, fill="#FFD700", anchor="mm")
        
        # 2. "Receives the Blessing:" (Subtext)
        draw.text((W/2, H*0.26), "receives the Nadar:", font=font_mean, fill="#DDDDDD", anchor="mm")

        # 3. Salok (Middle - White & Glowing)
        lines = textwrap.wrap(data['text'], width=25) 
        y_text = H * 0.45
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_text)
            draw.text((W/2, y_text), line, font=font_text, fill="white", anchor="mm")
            y_text += bbox[3] - bbox[1] + 25 

        # 4. Meaning (Bottom - Light Gold)
        lines_mean = textwrap.wrap(data['mean'], width=40)
        y_mean = y_text + 60
        for line in lines_mean:
            bbox = draw.textbbox((0, 0), line, font=font_mean)
            draw.text((W/2, y_mean), line, font=font_mean, fill="#FCEeb5", anchor="mm")
            y_mean += bbox[3] - bbox[1] + 15

        # 5. Footer Branding (Sis Ganj to Anandpur Reference)
        footer_line1 = "350th Martyrdom Anniversary | Guru Tegh Bahadur Ji"
        footer_line2 = "Sis Ganj Sahib • Anandpur Sahib"
        
        draw.text((W/2, H*0.88), footer_line1, font=font_small, fill="#FFD700", anchor="mm")
        draw.text((W/2, H*0.92), footer_line2, font=font_small, fill="#FFFFFF", anchor="mm")

        return img
    except Exception as e:
        st.error(f"Image Error: {e}")
        return None

# --- 4. UI LAYOUT (The Outstanding Part) ---

st.markdown("<h1 style='margin-bottom: -15px;'>✨ NADAR ✨</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #CCCCCC; margin-bottom: 30px;'>The 9th Light: Receive Your Blessing</h3>", unsafe_allow_html=True)

# Input Field
name_input = st.text_input("Enter Your Name:", placeholder="E.g. Karan Singh")

# The Golden Button
if st.button("🌹 Receive My Blessing 🌹", use_container_width=True):
    if name_input:
        with st.spinner("Connecting to History..."):
            # Logic
            selection = random.choice(saloks_data)
            final_img = create_poster(name_input, selection)
            
            if final_img:
                st.success(f"Waheguru Ji Mehar Karein, {name_input} 🙏")
                
                # Show Image
                st.image(final_img, caption=f"Nadar for {name_input}", use_column_width=True)
                
                # Prepare Download
                buf = io.BytesIO()
                final_img.save(buf, format="JPEG", quality=95)
                byte_im = buf.getvalue()
                
                col1, col2 = st.columns([1, 20]) # Layout trick
                
                st.download_button(
                    label="📥 Download HD Poster (For Status)",
                    data=byte_im,
                    file_name=f"Nadar_{name_input}.jpg",
                    mime="image/jpeg",
                    use_container_width=True
                )
                
                # Viral Sharing Text
                st.text_area("Copy Message to Share:", 
                             f"✨ 350th Shaheedi Purab Special ✨\n\nMaine Guru Tegh Bahadur Ji ki 'Nadar' (Blessing) receive ki hai.\nDekhiye aapke liye kaunsa sandesh aaya hai 👇\n\n[YOUR_LINK_HERE]\n\n#Nadar #The9thLight #Sikhi",
                             height=150)
                
                st.balloons()
    else:
        st.warning("Please enter your name to receive the blessing.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray; font-size: 12px;'>Dedicated to the Supreme Sacrifice of Hind Di Chadar.<br>Developed by Karan (Chitkara University)</div>", unsafe_allow_html=True)