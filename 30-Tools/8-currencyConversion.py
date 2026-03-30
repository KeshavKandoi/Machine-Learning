from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, ToolMessage
import requests
import os
from dotenv import load_dotenv
from typing import Annotated
from langchain_core.tools import InjectedToolArg, tool


load_dotenv() 

@tool
def ExchangeCurrency(base_currency:str,target_currency:str)->float:

  """ This is fetch the currency convertor using url and api and provide the data
  """

  url=f"https://v6.exchangerate-api.com/v6/941900b9e04956eef2524b7f/pair/{base_currency}/{target_currency}"

  response=requests.get(url)
  return response.json()


result=ExchangeCurrency.invoke({"base_currency":"USD","target_currency":"INR"})

# print(result)

@tool
def multiply(base_value:int,target_value:Annotated[float,InjectedToolArg])->float:
  """ given currency convertor rate use this and calculate the value using this function
  """

  return base_value*target_value

result2=multiply.invoke({"base_value":123,"target_value":232.2})

# print(result2)


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


llm_with_tools=llm.bind_tools([ExchangeCurrency,multiply])


messages=[HumanMessage('what is the conversion factor between USD and INR, and based on that can you convert 10 USD into INR')]




while True:
    ai_message = llm_with_tools.invoke(messages)

    # If no tool call → final answer
    if not ai_message.tool_calls:
        print("\nFinal Answer:\n")
        print(ai_message.content)
        break

    # Add AI message
    messages.append(ai_message)

    # Execute all tool calls
    for tool_call in ai_message.tool_calls:
        tool_name = tool_call["name"]
        args = tool_call["args"]

        if tool_name == "ExchangeCurrency":
            result = ExchangeCurrency.invoke(args)

        elif tool_name == "multiply":
            result = multiply.invoke(args)

        # Send result back to LLM
        messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            )
        )