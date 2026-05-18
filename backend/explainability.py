import cv2
import numpy as np
import torch
import torchvision.models as models
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from backend.analyze_face import analyze_face


def generate_gradcam(img_path: str, output_path: str = "outputs/gradcam_output.png") -> str:
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.eval()

    target_layers = [model.layer4[-1]]

    image = cv2.imread(img_path)

    analysis = analyze_face(img_path)
    region = analysis["face_region"]

    x = region["x"]
    y = region["y"]
    w = region["w"]
    h = region["h"]

    face_crop = image[y:y + h, x:x + w]

    image_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (224, 224))

    rgb_float = np.float32(image_resized) / 255.0

    input_tensor = torch.tensor(rgb_float).permute(2, 0, 1).unsqueeze(0)

    cam = GradCAM(model=model, target_layers=target_layers)
    grayscale_cam = cam(input_tensor=input_tensor, targets=[ClassifierOutputTarget(0)])
    grayscale_cam = grayscale_cam[0, :]

    visualization = show_cam_on_image(rgb_float, grayscale_cam, use_rgb=True)

    visualization_bgr = cv2.cvtColor(visualization, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, visualization_bgr)

    return output_path


if __name__ == "__main__":
    path = generate_gradcam("../demo_examples/test.jpg")
    print(f"Saved Grad-CAM visualization")