import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd

from ocr_utils import preprocess_image, extract_text_tesseract, extract_text_google_vision
from text_processing import clean_and_tokenize
from ner_extractor import extract_entities

st.title("📄 Medical History Extraction App")

image_type = st.radio("Select Image Type:", ("Printed", "Handwritten"))
uploaded_file = st.file_uploader("Upload Prescription Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    st.image(image_np, caption="Uploaded Image", use_column_width=True)
    st.write("🔧 Preprocessing Image (Grayscale)...")
    processed_image = preprocess_image(image_np)
    st.image(processed_image, caption="Grayscale Image", use_column_width=True)

    st.write("🔍 Extracting Text...")
    if image_type == "Printed":
        extracted_text = extract_text_tesseract(processed_image)
    else:
        extracted_text = extract_text_google_vision(processed_image)
    
    st.text_area("Extracted Text", extracted_text, height=200)

    st.write("🧹 Preprocessing Text...")
    cleaned_text = clean_and_tokenize(extracted_text)

    st.write("🧠 Running Named Entity Recognition...")
    df_entities = extract_entities(cleaned_text)
    st.dataframe(df_entities)

    if st.button("💾 Save to CSV"):
        df_entities.to_csv("extracted_medical_data.csv", index=False)
        st.success("Saved as extracted_medical_data.csv")
