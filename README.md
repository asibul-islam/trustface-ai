# TrustFace AI

TrustFace AI is a research-inspired prototype for trustworthy facial AI analysis. The system combines facial attribute estimation, image quality assessment, explainable AI, and robustness testing to explore reliability and trust in facial analytics systems.

---

## Motivation

Facial AI systems are increasingly used in identity verification, age estimation, online safety, and biometric applications. However, facial analytics can be affected by:

- image quality degradation,
- appearance changes,
- compression artifacts,
- blur,
- brightness variation,
- adversarial manipulation,
- and real-world environmental conditions.

TrustFace AI explores how trust-aware analysis and interpretable outputs can support research in reliable and explainable facial AI systems.

---

## Current Features

### Facial Analysis
- Facial age estimation
- Minor/adult age group detection
- Gender estimation
- Emotion estimation
- Face detection confidence

### Trust & Quality Assessment
- Biometric trust score
- Risk level assessment
- Blur detection
- Brightness analysis
- Quality-aware trust penalties

### Explainable AI
- Grad-CAM explainability heatmaps
- Facial attention visualization
- Face region extraction
- Eye landmark visualization

### Robustness Evaluation
- Perturbation testing pipeline
- Blur robustness testing
- Brightness robustness testing
- JPEG compression robustness testing
- Trust score comparison under perturbations

### System Features
- Interactive Streamlit frontend
- JSON result export
- Batch image analysis
- Automated visual report generation

---

## System Architecture

```text
Image Upload
      ↓
Facial Attribute Analysis
      ↓
Image Quality Assessment
      ↓
Trust Score Calculation
      ↓
Explainability Heatmap Generation
      ↓
Robustness Evaluation
      ↓
Visual Report Generation
```

---

## Tech Stack

- Python
- Streamlit
- DeepFace
- PyTorch
- OpenCV
- Grad-CAM
- Matplotlib

---

## Sample TrustFace AI Report

![TrustFace AI Report](backend/outputs/trustface_report.png)

---

## Explainability Heatmap

TrustFace AI uses Grad-CAM explainability visualization to highlight facial regions most influential to the model.

![GradCAM Output](backend/outputs/gradcam_output.png)

---

## Perturbation Robustness Testing

TrustFace AI evaluates how image perturbations affect biometric trust estimation.

Tested perturbations include:
- Original image
- Blurred image
- Darkened image
- Brightened image
- JPEG-compressed image

![Perturbation Trust Scores](backend/outputs/perturbation_trust_scores.png)

---

## Research Context

This project is inspired by research directions in:

- trustworthy biometric AI,
- facial manipulation robustness,
- explainable AI,
- image forensics,
- biometric reliability,
- and AI safety.

TrustFace AI is intended only as a research prototype and educational exploration system.

---

## Disclaimer

This system is NOT intended for:
- real-world identity verification,
- age verification,
- law enforcement,
- surveillance,
- hiring decisions,
- or high-stakes automated decision making.

The project is designed solely for research exploration and educational purposes.