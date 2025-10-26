# save as test_backend.py in repo root
import requests, base64, os, sys, json
URL = "http://127.0.0.1:8000/debug/cam"
mp4 = sys.argv[1]
with open(mp4, "rb") as f:
    r = requests.post(URL, files={"file": (os.path.basename(mp4), f, "video/mp4")})
data = r.json()
print(json.dumps(data, indent=2)[:800])
if data.get("explanations"):
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/heatmap0.jpg","wb") as out:
        out.write(base64.b64decode(data["explanations"][0]["heatmap_b64"]))
    print("Saved outputs/heatmap0.jpg")
