

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict,Annotated,Optional,Literal
from pydantic import BaseModel,Field

load_dotenv()
  
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

json_schema={
    "title": "Review",
    "type": "object",
    "properties": {
        "key_themes": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Write down all the key themes discussed in the review"
        },
        "summary": {
            "type": "string",
            "description": "A brief summary of the review"
        },
        "sentiment": {
            "type": "string",
            "enum": ["pos", "neg"],
            "description": "Return sentiment of the review either positive or negative"
        },
        "pros": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Write down all the pros inside a list",
            "default": None
        },
        "cons": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Write down all the cons inside a list",
            "default": None
        },
        "name": {
            "type": "string",
            "description": "Write the name of the reviewer",
            "default": None
        }
    },
    "required": ["key_themes", "summary", "sentiment"]
}



structured_model = model.with_structured_output(json_schema)

result = structured_model.invoke("""The hardware is great, but the software feels bloated.
There are too many pre-installed apps that I cant remove.
Also, the UI looks outdated compared to other brands.
Hoping for a software update to fix this.
                                 
Review by K.Kandoi                    """)

print(result)
print(result['name'])
