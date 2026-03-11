# FOR CREATING ENVIRONMENT
# python -m venv venv
# source venv/bin/activate

# ZERO SHOT PROMPTING

# CODE in OPENAI but api key=gemini

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),  # your Gemini API key
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "user", "content": "Who is Modi?"}
    ]
)

print(response.choices[0].message.content)