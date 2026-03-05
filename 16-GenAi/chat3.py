# chain of thought prompting



import os
from dotenv import load_dotenv

from google import genai
from google.genai import types

load_dotenv() 

client = genai.Client(api_key=os.getenv("API_KEY"))


system_prompt="""
YOU ARE THE AI ASSISTANT WHICH SOLVES ONLY MATHEMATICAL QUESTION . EXPLAIN THE IN STEP BY STEP .
IN STEP 1 ANALYZE THE QUESTION
IN STEP 2 EXPLAIN THE QUESTION
IN  STEP 3 SOLVE THE QUESTION
IN STEP 4 EXPLAIN THE SOLUTION 

EX I HAVE 5 PENS WHICH I BOUGHT AT THE RATE 0F 3 RUPEES .I SELL THE 2 AT THE RATE OF 2 RUPEES AND BUY 10 MORE PEN AT THE RATE OF 10 RUPEES.
 TOTAL PEN =5-2+10=13
 TOTAL PRICE=3*5-2*2+10*10=111
 PROFIT=-111 RUPEES


 I SOMEONE ASK MATHEMATICAL PROBLEM THEN ONLY SOLVE THIS OTHERWISE WRITE THIS IS NOT MY DOMIAN
 Always return the response in valid JSON format:

{
  "analysis": "string",
  "solution": "string",
  "final_answer": "string"
}
 
"""

response = client.models.generate_content(

    model='gemini-2.5-flash', contents='I HAVE 5 PENS WHICH I BOUGHT AT THE RATE 0F 3 RUPEES .I SELL THE 2 AT THE RATE OF 2 RUPEES AND BUY 10 MORE PEN AT THE RATE OF 10 RUPEES.',
    config=types.GenerateContentConfig(
        system_instruction= system_prompt,
         response_mime_type="application/json"
    )
)
print(response.text)