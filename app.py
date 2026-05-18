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
        temp_file.write(uploaded_file.read())
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

            st.success("Analysis complete.")

            st.markdown("## Trust Summary")

            m1, m2, m3, m4 = st.columns([1, 1, 1, 2])
            m1.metric("Estimated Age", analysis["estimated_age"])
            m2.metric("Age Group", analysis["age_group"])
            m3.metric("Trust Score", f"{analysis['biometric_trust_score']}/100")
            m4.metric("Risk Level", analysis["risk_level"])

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