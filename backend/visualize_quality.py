import cv2
import matplotlib.pyplot as plt
from analyze_face import analyze_face

img_path = "../demo_examples/test.jpg"

analysis = analyze_face(img_path)

image = cv2.imread(img_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# DeepFace stores face region inside the raw output, so for now we will draw a simple central box placeholder.
region = analysis["face_region"]

x1 = region["x"]
y1 = region["y"]
x2 = x1 + region["w"]
y2 = y1 + region["h"]

cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (0, 255, 0), 8)

left_eye = tuple(region["left_eye"])
right_eye = tuple(region["right_eye"])

cv2.circle(image_rgb, left_eye, 18, (255, 0, 0), -1)
cv2.circle(image_rgb, right_eye, 18, (255, 0, 0), -1)

label = f"Age: {analysis['estimated_age']} | {analysis['risk_level']}"

cv2.putText(
    image_rgb,
    label,
    (x1, max(y1 - 30, 40)),
    cv2.FONT_HERSHEY_SIMPLEX,
    2,
    (0, 255, 0),
    5
)

plt.figure(figsize=(8, 8))
plt.imshow(image_rgb)
plt.title(f"Trust Score: {analysis['biometric_trust_score']}/100 | Risk: {analysis['risk_level']}")
plt.axis("off")

plt.savefig("outputs/face_visualization.png", bbox_inches="tight", dpi=200)

print("Saved visualization")