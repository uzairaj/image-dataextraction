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


# Streamlit UI
st.header("Invoice OCR")

# File uploader for multiple images
uploaded_file = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])

# Input prompt for AI models
input_prompt = """
Act as an OCR expert.
You will receive an image of an invoice from any domain (finance, healthcare, retail, logistics, restaurant, etc.)
Your task is to extract all text exactly as it appears on the invoice, without modifying values..
Present the information in a structured JSON format with key-value pairs.
Do not include any additional explanations, commentary, or unnecessary text—only return the JSON response
"""
promp= '''
You are an expert in understanding invoices.
You will receive an image of an invoice.
Your task is to extract all invoice information and present it in a structured JSON format with key-value pairs.
Do not include any additional explanations, commentary, or unnecessary.

'''


def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


def get_gemini_response(input_prmp,image):
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        response = model.generate_content([input_prmp,image[0]])
        print('Gemini')
        print(response)
        return response.text
    except Exception as e:
        st.error(f"Gemini API error: {e}")
        return None

if st.button("Extract Invoice Data"):
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        try:
            
            image_data = input_image_setup(uploaded_file)
            response=get_gemini_response(promp,image_data)

            if response:
                st.subheader(f"Extracted Data")
                try:
                    st.json(json.loads(response))
                except:
                    st.write(response)
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")
