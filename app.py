import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import json
import pandas as pd
import base64
from google.generativeai.types import GenerationConfig
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")

gemini_config = GenerationConfig(temperature=0.2)

# Streamlit UI
st.header("Invoice Data Extractor")

# File uploader for multiple images
uploaded_files = st.file_uploader("Upload invoice images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Input prompt for AI models
input_prompt = """
Act as an expert in OCR technology.
You will receive an image of an invoice from any domain (e.g., finance, healthcare, retail, logistics, restaurant, etc.)
Your task is to extract all information present in the invoice while preserving the structure and relationships between data fields.
Present the extracted information in a structured JSON format with key-value pairs.
Just return json, no extra statements or texts.
"""
promp= 'Act as an OCR expert, extracts invoice data from the provided image and return a json response'


def prepare_image_gemini(uploaded_file):
    """Convert uploaded file to a PIL image for Gemini API."""
    try:
        image = Image.open(uploaded_file)
        return image
    except Exception as e:
        st.error(f"Error processing image for Gemini: {e}")
        return None

def get_gemini_response(prompt, image_data):
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash", generation_config=gemini_config)
        response = model.generate_content([input_prompt, image_data])
        print('Gemini')
        print(response)
        return response.text
    except Exception as e:
        st.error(f"Gemini API error: {e}")
        return None

if st.button("Extract Invoice Data") and uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            
            ##update_image = enhance_image(uploaded_file)
            image_data = prepare_image_gemini(uploaded_file)
            response = get_gemini_response(promp, image_data)

            if response:
                st.subheader(f"Extracted Data for {uploaded_file.name}")
                try:
                    st.json(json.loads(response))
                except:
                    st.write(response)
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")
