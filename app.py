from PIL import Image, ImageOps
import streamlit as st
import tempfile
import os

from backend.analyze_face import analyze_face
from backend.explainability import generate_gradcam


st.set_page_config(
    page_title="TrustFace AI",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
# TrustFace AI

**A research-inspired prototype for trustworthy facial AI analysis.**

Upload a face image to estimate facial attributes, image quality, biometric trust score, and generate an explainability heatmap.
""")

st.info(
    "Research prototype only. Not intended for real-world identity verification, age verification, "
    "law enforcement, or high-stakes decisions."
)

uploaded_file = st.file_uploader(
    "Upload a face image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        image = Image.open(uploaded_file)

        # Fix iPhone/EXIF rotation
        image = ImageOps.exif_transpose(image)

        # Convert to RGB so it saves safely as JPG
        image = image.convert("RGB")

        image.save(temp_file.name, format="JPEG")
        image_path = temp_file.name

    left, right = st.columns([1, 2])

    with left:
        st.subheader("Uploaded Image")
        st.image(image_path, use_container_width=True)

    with right:
        st.subheader("Run Analysis")

        if st.button("Analyze Image", type="primary"):
            with st.spinner("Analyzing facial attributes and image quality..."):
                analysis = analyze_face(image_path)

            # Format labels for cleaner UI and JSON display
            analysis["dominant_emotion"] = analysis["dominant_emotion"].capitalize()
            analysis["dominant_gender"] = analysis["dominant_gender"].capitalize()

            st.success("Analysis complete.")

            st.markdown("## Trust Summary")

            row1_col1, row1_col2, row1_col3 = st.columns(3)

            row1_col1.metric("Estimated Age", analysis["estimated_age"])
            row1_col2.metric("Age Group", analysis["age_group"])
            row1_col3.metric("Predicted Gender", analysis["dominant_gender"])

            row2_col1, row2_col2, row2_col3 = st.columns([1, 1, 1.5])

            row2_col1.metric("Emotion", analysis["dominant_emotion"])
            row2_col2.metric("Trust Score", f"{analysis['biometric_trust_score']}/100")
            row2_col3.metric("Risk Level", analysis["risk_level"])

            st.markdown("## Image Quality")
            q1, q2, q3 = st.columns([2, 1, 2])
            q1.metric("Blur Status", analysis["image_quality"]["blur_status"])
            q2.metric("Brightness", analysis["image_quality"]["brightness"])
            q3.metric("Brightness Status", analysis["image_quality"]["brightness_status"])

            with st.spinner("Generating explainability heatmap..."):
                gradcam_path = generate_gradcam(
                    image_path,
                    output_path="backend/outputs/gradcam_output.png"
                )

            st.markdown("## Explainability")
            c1, c2 = st.columns(2)

            with c1:
                st.image(image_path, caption="Original Image", use_container_width=True)

            with c2:
                st.image(gradcam_path, caption="Grad-CAM Heatmap", use_container_width=True)

            with st.expander("View full JSON result"):
                st.json(analysis)

            st.caption(analysis["research_note"])

    os.remove(image_path)