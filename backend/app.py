from fastapi import FastAPI, UploadFile, File
import tempfile, numpy as np
from detectors.faces import extract_frames, face_crops
from inference import score_rgb_crop, cam_on_rgb

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/debug/cam")
async def debug_cam(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
        f.write(await file.read())
        tmp = f.name

    frames = extract_frames(tmp, fps=2, max_frames=12)
    scores, explanations = [], []

    for i, fp in enumerate(frames):
        crops = face_crops(fp, out_size=112)
        if not crops:
            continue
        rgb = crops[0]
        scores.append(score_rgb_crop(rgb))
        if len(explanations) < 6:
            explanations.append({
                "frame_id": i,
                "note": "Grad-CAM",
                "heatmap_b64": cam_on_rgb(rgb)
            })

    video_score = float(np.mean(scores)) if scores else 0.5
    return {"video_score": video_score,
            "explanations": explanations,
            "frames_checked": len(frames)}

# Alias so clients can POST to /score if needed
@app.post("/score")
async def score_alias(file: UploadFile = File(...)):
    return await debug_cam(file)
