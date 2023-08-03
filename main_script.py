import streamlit as st
import requests
from azure_ocr import GetTextRead
from azure_translator import translate_text
import os
import cv2
import numpy as np

# Custom CSS style
cus_css = """
    body {
        color: #333;
        font-family: Arial, sans-serif;
        background-color: #f2f2f2;
        background-color: #f2f2f2;
        background-image: repeating-linear-gradient(45deg, transparent, transparent 20px, #c0c0c0 20px, #c0c0c0 40px);
    }
    .stButton {
        background-color: #007BFF !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 5px !important;
    }
    .stSelectbox {
        background-color: #fff !important;
        color: #333 !important;
        font-weight: bold !important;
        border-radius: 5px !important;
    }
    """

# Read the contents of the CSS file

# Apply custom CSS
st.markdown(f"<style>{cus_css}</style>", unsafe_allow_html=True)


# Streamlit app title and instructions
st.title("Multilingual OCR and Translator from Azure Cognitive Services")

# Choose the capture method
capture_method = st.radio("Choose capture method:", ("Capture from Webcam", "Upload Image"))

if capture_method == "Capture from Webcam":
    # Second field for webcam capture
    st.subheader("Take a picture from webcam")
    btn_camera_capture = st.button("Capture Picture")

    if btn_camera_capture:
        # Code to capture picture from webcam
        # Use cv2.VideoCapture to capture an image from the webcam
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        # Convert the BGR frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Save the captured image to a temporary file
        image_path = "temp_image.jpg"
        cv2.imwrite(image_path, frame)

        # Display the captured image in the frontend
        st.image(frame, channels="RGB", use_column_width=True)

    
elif capture_method == "Upload Image":
    # First field for image upload
    st.subheader("Upload your files here")
    uploaded_file = st.file_uploader("_____", type=["jpg", "jpeg", "png", "pdf"])

    if uploaded_file is not None:
        # Save the uploaded image to a temporary file
        image_path = "temp_image.jpg"
        with open(image_path, "wb") as f:
            f.write(uploaded_file.read())

# Process the image if available
if "image_path" in locals():
    # Call the OCR function and get the extracted text
    uf = image_path
    extracted_text = GetTextRead(uf)

    # Delete the temporary image file
    #os.remove(image_path)
    # Display the extracted text
    if extracted_text:
        st.subheader("Extracted Text:")
        #st.write(extracted_text)
        lines = extracted_text.split("\n")
        for line in lines:
            st.write(line)
        
        # Dictionary mapping language codes to full names
        language_names = {
        "en": "English",
        "fr": "French",
        "zu": "Zulu",
        "es": "Spanish",
        "it": "Italian",
        "ar": "Arabic",
        "hi": "Hindi",
        "ml": "Malayalam",
        "zh-Hans": "Simplified Chinese",
        }


       # Third field for language selection
        target_languages = list(language_names.keys())  # Use the list of keys from the dictionary
        target_language = st.selectbox("Select target language for translation",[language_names[code] for code in target_languages])
        for code in target_languages:
            if language_names[code]==target_language:
                print(code)

        for k, v in language_names.items():
            if v == target_language:
                target_language_code = k
                print(target_language_code)


        # Call the translation function and get the translated text
        translator_api_key = "f1fa0447cb344041bef0921f0cf06bbc"
        translator_api_region = "eastasia"

        translation_response = translate_text(translator_api_key, translator_api_region, extracted_text, [target_language_code])

        if translation_response:
            # Display the translated text
            translated_text = translation_response[0]['translations'][0]['text']
            st.subheader("Translated Text:")
            #st.write(translated_text)
            lines = translated_text.split("\n")
            for line in lines:
                st.write(line)
        else:
            st.error("Translation failed. Please try again later.")
    else:
        st.error("Text extraction failed.")

        
    