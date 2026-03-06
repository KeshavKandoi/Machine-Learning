# FOR CREATING ENVIRONMENT
# python -m venv venv
# source venv/bin/activate



# ZERO SHORT PROMPTING

import os
from dotenv import load_dotenv

from google import genai
from google.genai import types

load_dotenv() 

client = genai.Client(api_key=os.getenv("API_KEY"))

response = client.models.generate_content(
    model='gemini-2.5-flash', contents='Who is modi ?'
)
print(response.text)