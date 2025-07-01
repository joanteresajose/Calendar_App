import os
import requests
from dotenv import load_dotenv
import re

# Load environment variables from .env if present
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'  # Groq's OpenAI-compatible endpoint

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in environment or .env file.")

def extract_json_from_text(text):
    # Remove code block markers if present
    match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if match:
        text = match.group(1)
    else:
        # Fallback: try to find the first {...} block
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if match:
            text = match.group(1)
    return text

def extract_intent_entities(user_message: str) -> dict:
    """
    Calls Groq API to extract intent and entities from the user message.
    Returns a dict with keys: 'intent', 'entities'.
    """
    prompt = (
        "You are a helpful assistant for booking Google Calendar appointments. "
        "Extract the user's intent (e.g., book_appointment, check_availability, cancel_appointment) "
        "and all relevant entities (date, time, participants, etc.) from the following message. "
        "Respond ONLY with a valid JSON object with keys 'intent' and 'entities', and nothing else.\n"
        f"Message: {user_message}"
    )
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {GROQ_API_KEY}'
    }
    data = {
        "model": "llama3-8b-8192",  # Or another Groq-supported model
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for booking Google Calendar appointments."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.2
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    try:
        text = result['choices'][0]['message']['content']
        print("Groq LLM raw response:", text)  # Debug print
        text = extract_json_from_text(text)
        import json as pyjson
        return pyjson.loads(text)
    except Exception as e:
        return {"intent": "unknown", "entities": {}, "error": str(e)}
