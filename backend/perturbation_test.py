import cv2
import os
import json

from analyze_face import analyze_face


img_path = "../demo_examples/test.jpg"
output_dir = "outputs/perturbations"
os.makedirs(output_dir, exist_ok=True)

image = cv2.imread(img_path)

variants = {}

variants["original"] = image
variants["blurred"] = cv2.GaussianBlur(image, (21, 21), 0)
variants["darkened"] = cv2.convertScaleAbs(image, alpha=0.6, beta=0)
variants["brightened"] = cv2.convertScaleAbs(image, alpha=1.4, beta=20)

compression_path = os.path.join(output_dir, "compressed.jpg")
cv2.imwrite(compression_path, image, [cv2.IMWRITE_JPEG_QUALITY, 35])
variants["compressed"] = cv2.imread(compression_path)

all_results = []

for name, variant in variants.items():
    variant_path = os.path.join(output_dir, f"{name}.jpg")
    cv2.imwrite(variant_path, variant)

    print(f"\nAnalyzing {name} image...")
    analysis = analyze_face(variant_path)

    all_results.append({
        "variant": name,
        "image_path": variant_path,
        "analysis": analysis
    })

    print(f"Age: {analysis['estimated_age']}")
    print(f"Trust Score: {analysis['biometric_trust_score']}")
    print(f"Risk Level: {analysis['risk_level']}")
    print(f"Image Quality: {analysis['image_quality']}")

with open("outputs/perturbation_results.json", "w") as f:
    json.dump(all_results, f, indent=4)

print("\nSaved perturbation results")