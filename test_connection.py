import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise SystemExit("API key not found!")

print("Sending a simple request to Gemini...", flush=True)

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="Reply with exactly: FlowNexa connected."
    )

    print("Gemini replied:", response.text)

except Exception as error:
    print("Request failed:", type(error).__name__, error)

# The connection file determines if flownexa can connect to google api key