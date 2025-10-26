import cv2, numpy as np, os, tempfile, subprocess, glob

_MODEL_PATH = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "..", "models",
    "face_detection_yunet_2023mar.onnx"
))

detector = cv2.FaceDetectorYN.create(
    model=_MODEL_PATH,
    config="",
    input_size=(320, 320),
    score_threshold=0.6,
    nms_threshold=0.3,
    top_k=5000
)

def extract_frames(tmp_video: str, fps: int = 3, max_frames: int = 90):
    out_dir = tempfile.mkdtemp()
    cmd = [
        "ffmpeg", "-y", "-i", tmp_video,
        "-vf", f"fps={fps},scale=640:-1",
        "-qscale:v", "2", os.path.join(out_dir, "f_%05d.jpg")
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, check=False)
    return sorted(glob.glob(os.path.join(out_dir, "f_*.jpg")))[:max_frames]

def face_crops(frame_path: str, out_size: int = 112):
    img = cv2.imread(frame_path)
    if img is None:
        return []
    h, w = img.shape[:2]
    detector.setInputSize((w, h))
    ok, faces = detector.detect(img)
    crops = []
    if ok and faces is not None:
        for f in faces:
            x, y, ww, hh = f[:4].astype(int)
            x, y = max(0, x), max(0, y)
            ww, hh = min(w - x, ww), min(h - y, hh)
            if ww <= 0 or hh <= 0:
                continue
            crop = cv2.resize(img[y:y+hh, x:x+ww],
                              (out_size, out_size))
            crops.append(crop[:, :, ::-1])  # BGR→RGB
    return crops