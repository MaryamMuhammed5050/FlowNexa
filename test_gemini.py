import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise SystemExit("Gemini API key not found.")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=120000)
)

print("Sending request to Gemini...", flush=True)

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="""
    Analyse this request:
    I want to compare the prices of two phones.
    
    Return these details:
    - intent
    - item
    - quantity
    - execute_order

    Return JSON only.
    """,
    config=types.GenerateContentConfig(
    response_mime_type="application/json",
    thinking_config=types.ThinkingConfig(
        thinking_level="low"
    ),
    max_output_tokens=200
)
)

# Convert Gemini's JSON response into a Python dictionary
result = json.loads(response.text)

print(result)
print("\nDetected intent:", result["intent"])