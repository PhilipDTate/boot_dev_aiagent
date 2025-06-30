import os
from dotenv import load_dotenv
import sys
from google.genai import types
from google import genai



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

#Getting the prompt from the command line
input =sys.argv

#Checking the prompt
if len(input) == 1:
    exit(1)

user_prompt=' '.join(input[1:-1])
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]




client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

print(response.text)
if (input[-1]=="--verbose"):
    print("User prompt:", user_prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)