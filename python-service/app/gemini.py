import logging
import google.generativeai as genai
from google.generativeai import GenerativeModel
from .config import GEMINI_API_KEY, MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)

def generate_text_with_gemini(prompt: str) -> str:
    """Generates text using Vertex AI Gemini API."""
    try:
        model = GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        response.resolve()
        if response.text:
            return response.text
        else:
             logging.error("Gemini Response failed.")
             return "Gemini Response failed."

    except Exception as e:
        logging.error(f"Gemini API call error: {e}")
        return f"Error generating text: {e}"