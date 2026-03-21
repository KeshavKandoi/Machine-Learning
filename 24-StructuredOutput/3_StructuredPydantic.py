

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict,Annotated,Optional,Literal
from pydantic import BaseModel,Field

load_dotenv()
  
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class Review(BaseModel):
    
    key_themes:list[str]=Field(description="write down all the key themes discussed in the review")

    summary: str=Field(description="A brief summary of the review")

    sentiment:Literal["pos","neg"]=Field(description="Return sentiment of the review either negative,positiveor neutral")

    pros:Optional[list[str]]=Field(default=None,description="write down all the pros inside a list")

    cons:Optional[list[str]]=Field(default=None,description="Write down all the cons inside a list")

    name:Optional[str]=Field(default=None,description="write the name of the reviewer")



structured_model = model.with_structured_output(Review)

result = structured_model.invoke("""The hardware is great, but the software feels bloated.
There are too many pre-installed apps that I cant remove.
Also, the UI looks outdated compared to other brands.
Hoping for a software update to fix this.
                                 
Review by K.Kandoi                    """)

print(result)
print(result.name)
