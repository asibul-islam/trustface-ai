import cv2
import os


def assess_image_quality(img_path: str) -> dict:
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Image not found: {img_path}")

    image = cv2.imread(img_path)

    if image is None:
        raise ValueError("Could not read image. Please check the file format.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    height, width = image.shape[:2]
    brightness = gray.mean()

    if blur_score < 100:
        blur_status = "Potentially Blurry"
    else:
        blur_status = "Clear"

    if brightness < 60:
        brightness_status = "Too Dark"
    elif brightness > 200:
        brightness_status = "Too Bright"
    else:
        brightness_status = "Normal"

    return {
        "image_width": width,
        "image_height": height,
        "blur_score": round(float(blur_score), 2),
        "blur_status": blur_status,
        "brightness": round(float(brightness), 2),
        "brightness_status": brightness_status
    }