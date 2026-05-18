import cv2
import matplotlib.pyplot as plt

from analyze_face import analyze_face
from explainability import generate_gradcam


img_path = "../demo_examples/test.jpg"

analysis = analyze_face(img_path)
gradcam_path = generate_gradcam(img_path)

original = cv2.imread(img_path)
original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

gradcam = cv2.imread(gradcam_path)
gradcam = cv2.cvtColor(gradcam, cv2.COLOR_BGR2RGB)

region = analysis["face_region"]
x, y, w, h = region["x"], region["y"], region["w"], region["h"]

cv2.rectangle(original, (x, y), (x + w, y + h), (0, 255, 0), 8)

summary = (
    f"Age: {analysis['estimated_age']} ({analysis['age_group']})\n"
    f"Trust Score: {analysis['biometric_trust_score']}/100\n"
    f"Risk Level: {analysis['risk_level']}\n"
    f"Image Quality: {analysis['image_quality']['blur_status']}, "
    f"{analysis['image_quality']['brightness_status']}"
)

plt.figure(figsize=(12, 6))

plt.subplot(1, 3, 1)
plt.imshow(original)
plt.title("Detected Face")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(gradcam)
plt.title("Explainability Heatmap")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.text(0.05, 0.5, summary, fontsize=14, va="center")
plt.title("TrustFace AI Report")
plt.axis("off")

plt.tight_layout()
plt.savefig("outputs/trustface_report.png", bbox_inches="tight", dpi=200)

print("Saved report to backend/outputs/trustface_report.png")