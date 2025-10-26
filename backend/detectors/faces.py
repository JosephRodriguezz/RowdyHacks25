import cv2, numpy as np, os, tempfile, subprocess, glob

# --- Frame extraction ---
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

# --- SSD detector (Caffe model) ---
_MODEL_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "models"))
_SSD_PROTO = os.path.join(_MODEL_DIR, "deploy.prototxt")
_SSD_MODEL = os.path.join(_MODEL_DIR, "res10_300x300_ssd_iter_140000.caffemodel")

if not (os.path.exists(_SSD_PROTO) and os.path.exists(_SSD_MODEL)):
    raise FileNotFoundError(
        "OpenCV SSD face model missing. Download deploy.prototxt and "
        "res10_300x300_ssd_iter_140000.caffemodel into models/."
    )

_net = cv2.dnn.readNetFromCaffe(_SSD_PROTO, _SSD_MODEL)

def face_crops(frame_path: str, out_size: int = 112, conf_thresh: float = 0.6):
    img = cv2.imread(frame_path)
    if img is None:
        return []
    h, w = img.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    _net.setInput(blob)
    detections = _net.forward()

    crops = []
    for i in range(detections.shape[2]):
        conf = float(detections[0, 0, i, 2])
        if conf < conf_thresh:
            continue
        x1, y1, x2, y2 = (detections[0, 0, i, 3:7] * np.array([w, h, w, h])).astype(int)
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        if x2 > x1 and y2 > y1:
            crop = cv2.resize(img[y1:y2, x1:x2], (out_size, out_size))
            crops.append(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)) # contigous RGB
    return crops
