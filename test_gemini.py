import os
from dotenv import load_dotenv
from google import genai

# Load settings from the .env file
load_dotenv()

# Get the API key without displaying it
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise SystemExit("Error: Gemini API key was not found.")

# Connect to Gemini
client = genai.Client(api_key=api_key)

# Send a test request
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Reply with exactly: FlowNexa is connected to Gemini."
)

# Display Gemini's response
print(response.text)