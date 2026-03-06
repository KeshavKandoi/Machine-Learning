# FOR CREATING ENVIRONMENT
# python -m venv venv
# source venv/bin/activate

# ONE SHOT PROMPTING 



import os
from dotenv import load_dotenv

from google import genai
from google.genai import types

load_dotenv() 

client = genai.Client(api_key=os.getenv("API_KEY"))


system_prompt="""
YOU ARE THE AI ASSISTANT WHICH SOLVES ONLY MATHEMATICAL QUESTION . EXPLAIN THE QUESTION IN DETAIL 
EX-2+2=4
2,2,4 ARE REAL NUMBER .WE ARE  ADDING 2+2 .
IF SOMEONE ASK OTHER DOMAIN QUESTION WRITE THIS IS NOT MY DOMAIN 
"""

response = client.models.generate_content(
    model='gemini-2.5-flash', contents='30+3?',
    config={
        "system_instruction": system_prompt
    }
)
print(response.text)