# ToolBinding

from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import requests
import os
from dotenv import load_dotenv



load_dotenv() 


@tool
def multiply(a:int,b:int) -> int:
  """Multiply two numbers"""
  return a*b



llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

llm_with_tools=llm.bind_tools([multiply])


# response = llm_with_tools.invoke("What is 4 * 5?")
# response = llm_with_tools.invoke("can you multiply 5 and 10")
response = llm_with_tools.invoke("can you multiply 5 and 10")
# result=response.tool_calls[0]['args']
result=response.tool_calls[0]
# print(result)

print(multiply.invoke(result))