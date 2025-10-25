import streamlit as st, requests, base64
st.set_page_config(page_title="DeepDetechd", layout="centered")
st.title("DeepDetechd — Deepfake Detector (MVP)")

file = st.file_uploader("Upload a short video (≤15s)", type=["mp4","mov","webm"])
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
    st.write("Prediction:", "🟥 **FAKE**" if score >= th else "�� **REAL**")
    for ex in data.get("explanations", [])[:8]:
        b64 = ex.get("heatmap_b64")
        if b64:
            st.image(base64.b64decode(b64), caption=f'Frame {ex["frame_id"]}: {ex["note"]}')
