import numpy as np, torch, cv2
from torchvision import transforms
from torchvision.models import resnet18, ResNet18_Weights
from explain.cam import GradCAM, overlay_cam_on_image, encode_jpg_base64

_device = "cpu"
_model = resnet18(weights=None).to(_device).eval()
_target_layer = _model.layer4[-1].conv2

_pre = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((224, 224), antialias=True),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

def score_rgb_crop(rgb: np.ndarray) -> float:
    x = _pre(rgb).unsqueeze(0).to(_device)
    with torch.no_grad():
        prob = torch.softmax(_model(x), dim=1).max().item()
    return float(1.0 - prob)  # placeholder demo score

def cam_on_rgb(rgb: np.ndarray) -> str:
    x = _pre(rgb).unsqueeze(0).requires_grad_(True)
    cam = GradCAM(_model, _target_layer)
    try:
        heat = cam(x)
    finally:
        cam.remove_hooks()
    rgb_small = cv2.resize(rgb, (224, 224))
    overlay = overlay_cam_on_image(rgb_small, heat, alpha=0.45)
    return encode_jpg_base64(overlay)
