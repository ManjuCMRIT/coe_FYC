# app.py

import streamlit as st
from PIL import Image
import cv2
import numpy as np
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Document Scanner", layout="centered")

st.title("📄 Document Scanner")
st.write("Upload a document image, convert it to black & white, and download it as a PDF.")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

def convert_to_bw(image):
    # Convert PIL image to OpenCV format
    img = np.array(image)

    # Convert RGB to BGR
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive threshold for scanner effect
    bw = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return bw

def create_pdf(image_path, pdf_path):
    pdf = FPDF()
    pdf.add_page()

    # Fit image to A4 size
    pdf.image(image_path, x=10, y=10, w=190)

    pdf.output(pdf_path)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Convert to PDF"):
        bw_image = convert_to_bw(image)

        st.subheader("Black & White Scanned Image")
        st.image(bw_image, clamp=True, use_container_width=True)

        with tempfile.TemporaryDirectory() as tmpdir:
            image_path = os.path.join(tmpdir, "scanned.png")
            pdf_path = os.path.join(tmpdir, "document.pdf")

            # Save processed image
            cv2.imwrite(image_path, bw_image)

            # Create PDF
            create_pdf(image_path, pdf_path)

            # Download button
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_file,
                    file_name="scanned_document.pdf",
                    mime="application/pdf"
                )
