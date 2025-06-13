# ai_logic.py
import os
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

# Find and load .env variables
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)

# Retrieve the API key
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# Basic validation for API Key
if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_ACTUAL_GEMINI_API_KEY_HERE":
    raise RuntimeError(
        "GEMINI_API_KEY not found or invalid. "
        "Please replace 'YOUR_ACTUAL_GEMINI_API_KEY_HERE' "
        "with your actual Google Gemini API key in your .env file."
    )

# --- Gemini Model Initialization ---
model = None # Initialize model as None

def get_available_gemini_model():
    """
    Checks for available Gemini models that support generateContent method,
    prioritizing 'gemini-1.5-flash', then 'gemini-pro', then 'gemini-1.5-pro',
    then any other suitable model.
    """
    genai.configure(api_key=GOOGLE_API_KEY) # Configure here just before listing models

    # 1. Prioritize gemini-1.5-flash (more free-tier friendly)
    for m in genai.list_models():
        if m.name == 'models/gemini-1.5-flash' and 'generateContent' in m.supported_generation_methods:
            print(f"Prioritizing available model: {m.name}") # For debugging purposes
            return genai.GenerativeModel(m.name)

    # 2. Fallback to gemini-pro (older stable, often good free tier)
    for m in genai.list_models():
        if m.name == 'models/gemini-pro' and 'generateContent' in m.supported_generation_methods:
            print(f"Falling back to available model: {m.name}") # For debugging purposes
            return genai.GenerativeModel(m.name)

    # 3. Fallback to gemini-1.5-pro (your previously chosen, but more limited model)
    for m in genai.list_models():
        if m.name == 'models/gemini-1.5-pro' and 'generateContent' in m.supported_generation_methods:
            print(f"Falling back to available model: {m.name}") # For debugging purposes
            return genai.GenerativeModel(m.name)
            
    # 4. Final fallback to any other model supporting generateContent
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Using general suitable model: {m.name}") # For debugging purposes
            return genai.GenerativeModel(m.name)
            
    raise Exception(
        "No Gemini model found that supports 'generateContent'. "
        "Please ensure your API key is correct and valid, or check Google AI Studio for available models."
    )

try:
    model = get_available_gemini_model()
except Exception as e:
    # This exception will be propagated to Streamlit's main_app.py
    # if `ask_gemini` is called and `model` is None.
    print(f"FATAL ERROR in ai_logic.py: Could not initialize Gemini model. "
          f"Ensure API key is valid and models are accessible: {e}")
    model = None # Explicitly set model to None on failure

def ask_gemini(prompt: str) -> str:
    """
    Sends a prompt to the configured Gemini model and returns the text response.
    Returns Markdown-formatted text.
    """
    if model is None:
        return "❌ Gemini AI service is not available. Please check your API key and model access."
    
    if not prompt.strip():
        return "Please provide a valid input for explanation."

    try:
        response = model.generate_content(prompt)
        if response and response.candidates and len(response.candidates) > 0 and \
           response.candidates[0].content and response.candidates[0].content.parts and \
           len(response.candidates[0].content.parts) > 0:
            return response.candidates[0].content.parts[0].text
        else:
            return "❌ Gemini API Error: No valid response text found. The AI might not have generated content for this query."
    except Exception as e:
        return f"❌ Gemini API Call Failed: {e}\n\n" \
               "Possible issues: incorrect API key, rate limit exceeded, or model access problems. " \
               "Please ensure your GEMINI_API_KEY is correct and you have access to the selected model(s)."

