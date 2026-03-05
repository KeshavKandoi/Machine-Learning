import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))

system_prompt = """
You are an AI assistant that solves only mathematical questions.

If the problem does not contain enough information:
- Ask exactly one clarifying question.
- Do NOT solve yet.

If enough information is available:
- Solve step-by-step clearly.

Return output in valid JSON format:

{
  "analysis": "...",
  "final_answer": "..."
}
"""

# Original Question

original_question = "I am 10 years older than my sister. What is my sister’s age?"

# First Call
response1 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=original_question,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="application/json"
    )
)

print("First Response:")
print(response1.text)

parsed1 = json.loads(response1.text)

# Ask user for clarification
clarification = input("Answer the clarification question: ")

# Second Call with clarification included
response2 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"""
Original Question:
{original_question}

Clarification:
{clarification}

Now solve the problem completely.
""",
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="application/json"
    )
)

print("\nFinal Response:")
print(response2.text)
