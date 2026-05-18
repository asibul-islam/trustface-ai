import json
import matplotlib.pyplot as plt

with open("outputs/perturbation_results.json", "r") as f:
    results = json.load(f)

variants = [item["variant"] for item in results]
trust_scores = [item["analysis"]["biometric_trust_score"] for item in results]
ages = [item["analysis"]["estimated_age"] for item in results]

plt.figure(figsize=(8, 5))
plt.bar(variants, trust_scores)
plt.ylim(0, 100)
plt.title("Trust Score Under Image Perturbations")
plt.xlabel("Image Variant")
plt.ylabel("Biometric Trust Score")

plt.savefig("outputs/perturbation_trust_scores.png", bbox_inches="tight", dpi=200)

print("Saved chart")