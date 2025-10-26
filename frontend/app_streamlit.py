import streamlit as st
import requests
import base64
import random
import os


with open("assets/robobuddy.png", "rb") as img_file:
    b64_img = base64.b64encode(img_file.read()).decode()
img_url = f"data:image/jpeg;base64,{b64_img}"


st.set_page_config(page_title="DeepDetech'd", layout="centered")

st.markdown(f"""
<style>
@keyframes spiralMove {{
    0% {{
        transform: translate(0px, 0px) rotate(0deg);
    }}
    25% {{
        transform: translate(300px, 100px) rotate(90deg);
    }}
    50% {{
        transform: translate(600px, 300px) rotate(180deg);
    }}
    75% {{
        transform: translate(300px, 500px) rotate(270deg);
    }}
    100% {{
        transform: translate(0px, 300px) rotate(360deg);
    }}
}}

.spiral-bg {{
    position: fixed;
    top: 90;
    left: 5%;
    width: 100px;
    height: 100px;
    background-image: url('{img_url}');
    background-size: contain;
    background-repeat: no-repeat;
    animation: spiralMove 40s linear infinite;
    z-index: 0;
}}
</style>

<div class="spiral-bg"></div>
""", unsafe_allow_html=True)

# Neon Title
st.markdown("""
<h2 class="neon-title">
    DeepDetech'd — Deepfake Detector
</h2>
<style>
@keyframes neonPurplePulse {
    0%, 100% {
        text-shadow:
            0 0 5px #b366ff,
            0 0 10px #a64dff,
            0 0 15px #9933ff,
            0 0 20px #8000ff,
            0 0 25px #6600cc;
    }
    50% {
        text-shadow:
            0 0 8px #b366ff,
            0 0 15px #a64dff,
            0 0 22px #9933ff,
            0 0 30px #8000ff,
            0 0 35px #6600cc;
    }
}

.neon-title {
    text-align: center;
    color: #9933ff;
    font-weight: bold;
    letter-spacing: 1px;
    animation: neonPurplePulse 1.5s ease-in-out infinite alternate;
}
</style>
""", unsafe_allow_html=True)

# Credits
st.markdown("""
<p class="neon-credit">
    Created by Diego Saldana, Joseph Rodriguez, Gabriel Saldana, and Chloe Bruno
</p>
<style>
@keyframes neonDarkBluePulse {
    0%, 100% {
        text-shadow:
            0 0 5px #001f4d,
            0 0 10px #002966,
            0 0 15px #003366,
            0 0 20px #003366,
            0 0 25px #001a4d;
    }
    50% {
        text-shadow:
            0 0 8px #001f4d,
            0 0 15px #002966,
            0 0 22px #003366,
            0 0 30px #003366,
            0 0 35px #001a4d;
    }
}

.neon-credit {
    text-align: center;
    color: #001f4d;
    font-weight: bold;
    font-size: 1.2em;
    animation: neonDarkBluePulse 1.5s ease-in-out infinite alternate;
}
</style>
""", unsafe_allow_html=True)

# Generate randomized CSS and HTML for 200 stars across full screen
star_css = "\n".join([
    f".stationary-star.s{i} {{ top: {random.randint(0, 700)}px; left: {random.randint(-200, 1400)}px; }}"
    for i in range(1, 201)
])
star_html = "\n".join([
    f'<div class="stationary-star s{i}"></div>'
    for i in range(1, 201)
])

# Inject styles and stars
st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
    background: radial-gradient(circle at top left, #03000d 0%, #060018 40%, #000008 100%) !important;
    background-attachment: fixed;
    color: #e0e0ff;
    overflow: hidden;
}}

/* Shooting Stars */
.star-wrapper {{
    position: fixed;
    top: 0;
    left: 0;
    animation: shoot 3s ease-in-out infinite;
    z-index: -1;
}}
.star {{
    width: 5px;
    height: 5px;
    background: white;
    border-radius: 50%;
    box-shadow: 0 0 8px #ffffff, 0 0 12px #a066ff, 0 0 20px #9933ff;
    position: relative;
}}

@keyframes shoot {{
    0% {{ transform: translate(0, 0); opacity: 1; }}
    100% {{ transform: translate(1000px, 600px); opacity: 0; }}
}}

.star-wrapper.delay0 {{ animation-delay: 0s; top: -50px; left: -100px; }}
.star-wrapper.delay1 {{ animation-delay: 1s; top: -70px; left: -150px; }}
.star-wrapper.delay2 {{ animation-delay: 2s; top: -30px; left: -200px; }}
.star-wrapper.delay3 {{ animation-delay: 3s; top: -90px; left: -50px; }}
.star-wrapper.delay4 {{ animation-delay: 4s; top: -60px; left: -250px; }}
.star-wrapper.delay5 {{ animation-delay: 5s; top: -40px; left: -300px; }}
.star-wrapper.delay6 {{ animation-delay: 6s; top: -80px; left: -180px; }}
.star-wrapper.delay7 {{ animation-delay: 7s; top: -100px; left: -220px;}} 


/* Stationary Stars */
@keyframes pulse {{
    0%, 100% {{ box-shadow: 0 0 6px #ffffff; opacity: 0.8; }}
    50% {{ box-shadow: 0 0 12px #ffffff; opacity: 1; }}
}}
.stationary-star {{
    position: fixed;
    width: 3px;
    height: 3px;
    background: white;
    border-radius: 50%;
    animation: pulse 2s infinite ease-in-out;
    z-index: -1;
}}

{star_css}

/* Glass Container */
.block-container {{
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 3rem 2rem;
    box-shadow: 0 0 25px rgba(0,0,0,0.4);
    z-index: 2;
}}

/* Text */
h1, h2, h3, h4, h5, h6, p, label, span {{
    color: #e6e6fa !important;
}}

/* Metrics */
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
    color: #f5f5ff !important;
}}

/* Buttons */
div.stButton > button {{
    background: linear-gradient(135deg, #3f0071, #1b0033);
    color: white;
    border: 1px solid #663399;
    border-radius: 12px;
    padding: 0.6em 1.2em;
    transition: all 0.3s ease-in-out;
}}
div.stButton > button:hover {{
    background: linear-gradient(135deg, #5d00a0, #2a0060);
    transform: scale(1.05);
    border-color: #a066ff;
    box-shadow: 0 0 15px #a066ff55;
}}

/* Sliders & Uploaders */
section[data-testid="stFileUploader"] > div > div {{
    color: #FFA500 !important;
}}
.stSlider > div > div > div {{
    color: white !important;
}}

/* File Uploader Styling */
div.stFileUploader > div {{
    background: linear-gradient(135deg, #3f0071, #1b0033) !important;
    border: 1px solid #663399 !important;
    border-radius: 12px !important;
    padding: 0.6em 1.2em !important;
    text-align: center !important;
    color: white !important;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
}}
div.stFileUploader > div:hover {{
    background: linear-gradient(135deg, #5d00a0, #2a0060) !important;
    box-shadow: 0 0 15px #a066ff55;
    transform: scale(1.02);
}}
</style>

<!-- Shooting Stars -->
<div class="star-wrapper delay0"><div class="star"></div></div>
<div class="star-wrapper delay1"><div class="star"></div></div>
<div class="star-wrapper delay2"><div class="star"></div></div>
<div class="star-wrapper delay3"><div class="star"></div></div>

<!-- Stationary Stars -->
{star_html}
""", unsafe_allow_html=True)

# App Logic
file = st.file_uploader("Upload a short video (≤15s)", type=["mp4", "mov", "webm"])
th = st.slider("Decision threshold", 0.50, 0.99, 0.90, 0.01)

if st.button("Analyze") and file:
    with st.spinner("Scoring..."):
        r = requests.post(
            "http://localhost:8000/score",
            files={"file": (file.name, file.getvalue(), "application/octet-stream")}
        )
    data = r.json()
    score = float(data.get("video_score", 0.0))
    st.metric("Fake probability", f"{score:.2%}")
    st.write("Prediction:", " **FAKE**" if score >= th else " **REAL**")
    for ex in data.get("explanations", [])[:8]:
        b64 = ex.get("heatmap_b64")
        if b64:
            st.image(base64.b64decode(b64), caption=f'Frame {ex["frame_id"]}: {ex["note"]}')
