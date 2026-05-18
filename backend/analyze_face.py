from deepface import DeepFace
from backend.quality_checks import assess_image_quality
import json
import os


def analyze_face(img_path: str) -> dict:
    result = DeepFace.analyze(
        img_path=img_path,
        actions=["age", "gender", "emotion"],
        enforce_detection=False
    )

    data = result[0]
    face_confidence = float(data["face_confidence"])
    quality = assess_image_quality(img_path)
    trust_score = face_confidence * 100

    if quality["blur_status"] == "Potentially Blurry":
        trust_score -= 15

    if quality["brightness_status"] != "Normal":
        trust_score -= 10

    trust_score = max(0, min(100, round(trust_score, 2)))
    estimated_age = int(data["age"])

    if trust_score >= 80:
        risk_level = "Low Risk"
    elif trust_score >= 50:
        risk_level = "Moderate Risk"
    else:
        risk_level = "High Risk"

    if estimated_age < 18:
        age_group = "Minor"
        age_verification_risk = "Sensitive"
    else:
        age_group = "Adult"
        age_verification_risk = "Standard"

    return {
        "estimated_age": estimated_age,
        "age_group": age_group,
        "age_verification_risk": age_verification_risk,
        "dominant_gender": data["dominant_gender"],
        "dominant_emotion": data["dominant_emotion"],
        "face_confidence": round(face_confidence, 2),
        "biometric_trust_score": trust_score,
        "risk_level": risk_level,
        "image_quality": quality,
        "face_region": data["region"],
        "trust_score_explanation": (
            "The trust score is based on face detection confidence, with penalties for poor image quality "
            "such as blur or abnormal brightness."
        ),
        "research_note": (
            "This analysis estimates facial attributes and produces a preliminary biometric trust score. "
            "It is intended for research exploration in trustworthy facial AI, not for real-world identity "
            "or age verification decisions."
        )
    }


if __name__ == "__main__":
    img_path = "../demo_examples/test.jpg"

    analysis = analyze_face(img_path)

    print("\nTrustFace AI Analysis:\n")
    for key, value in analysis.items():
        print(f"{key}: {value}")

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "analysis_result.json"), "w") as f:
        json.dump(analysis, f, indent=4)

    print("Saved result to backend/outputs/analysis_result.json")