from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv() 

client = genai.Client(api_key=os.getenv("API_KEY"))



system_prompt="""


"""


response = client.models.generate_content(

    model='gemini-2.5-flash', 
    contents='',
    config=types.GenerateContentConfig(
        system_instruction= system_prompt,
         response_mime_type="application/json"
    )
)
print(response.text)