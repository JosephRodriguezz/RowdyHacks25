from typing import Optional
import torch, torch.nn.functional as F
import numpy as np, cv2, base64

class GradCAM:
    def __init__(self, model: torch.nn.Module,
                 target_layer: torch.nn.Module):
        self.model = model.eval()
        self.target_layer = target_layer
        self._acts = None
        self._grads = None
        self._fwd = target_layer.register_forward_hook(
            lambda m, i, o: setattr(self, "_acts", o.detach()))
        self._bwd = target_layer.register_full_backward_hook(
            lambda m, gi, go: setattr(self, "_grads", go[0].detach()))

    def remove_hooks(self):
        self._fwd.remove()
        self._bwd.remove()

    def __call__(self, x: torch.Tensor,
                 target_category: Optional[int] = None) -> np.ndarray:
        self.model.zero_grad(set_to_none=True)
        logits = self.model(x)
        if target_category is None:
            target_category = int(torch.argmax(logits, dim=1))
        logits[:, target_category].backward(retain_graph=True)
        acts, grads = self._acts[0], self._grads[0]
        weights = torch.mean(grads, dim=(1, 2))
        cam = F.relu(torch.sum(weights[:, None, None] * acts, dim=0))
        cam = (cam - cam.min()) / (cam.max() if cam.max() > 0 else 1)
        return cam.detach().cpu().numpy()

def overlay_cam_on_image(rgb: np.ndarray, cam: np.ndarray,
                         alpha: float = 0.45) -> np.ndarray:
    h, w = rgb.shape[:2]
    cam = cv2.resize(cam, (w, h))
    cam8 = (cam * 255).astype(np.uint8)
    heat = cv2.applyColorMap(cam8, cv2.COLORMAP_JET)
    heat = cv2.cvtColor(heat, cv2.COLOR_BGR2RGB)
    out = (alpha * heat + (1 - alpha) * rgb.astype(np.float32)) \
        .clip(0, 255).astype(np.uint8)
    return out

def encode_jpg_base64(rgb: np.ndarray, quality=90) -> str:
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    ok, buf = cv2.imencode(".jpg", bgr,
                           [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    return base64.b64encode(buf.tobytes()).decode() if ok else ""
