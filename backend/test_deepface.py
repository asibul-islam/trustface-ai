from deepface import DeepFace
import json
import os

img_path = "../demo_examples/test.jpg"
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

result = DeepFace.analyze(
    img_path=img_path,
    actions=['age', 'gender', 'emotion'],
    enforce_detection=False
)

data = result[0]
face_confidence = float(data["face_confidence"])
trust_score = round(face_confidence * 100, 2)

if trust_score >= 80:
    risk_level = "Low Risk"
elif trust_score >= 50:
    risk_level = "Moderate Risk"
else:
    risk_level = "High Risk"

estimated_age = int(data["age"])

if estimated_age < 18:
    age_group = "Minor"
    age_verification_risk = "Sensitive"
else:
    age_group = "Adult"
    age_verification_risk = "Standard"

analysis = {
    "estimated_age": data["age"],
    "age_group": age_group,
    "age_verification_risk": age_verification_risk,
    "dominant_gender": data["dominant_gender"],
    "dominant_emotion": data["dominant_emotion"],
    "face_confidence": round(face_confidence, 2),
    "biometric_trust_score": trust_score,
    "risk_level": risk_level,
    "research_note": "This analysis estimates facial attributes and produces a preliminary biometric trust score. It is intended for research exploration in trustworthy facial AI, not for real-world identity or age verification decisions."
}

print("\nTrustFace AI Analysis:\n")
for key, value in analysis.items():
    print(f"{key}: {value}")

with open(os.path.join(output_dir, "analysis_result.json"), "w") as f:
    json.dump(analysis, f, indent=4)

print("Saved result to backend/outputs/analysis_result.json")