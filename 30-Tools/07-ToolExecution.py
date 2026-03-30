# ToolBinding

from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, ToolMessage
import os
from dotenv import load_dotenv

load_dotenv() 


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b



llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

llm_with_tools = llm.bind_tools([multiply])



query = HumanMessage(content="can you multiply 3 with 1000")

messages = [query]


result = llm_with_tools.invoke(messages)
messages.append(result)


tool_call = result.tool_calls[0]
tool_result = multiply.invoke(tool_call["args"])



messages.append(
    ToolMessage(
        content=str(tool_result),
        tool_call_id=tool_call["id"]
    )
)



final = llm_with_tools.invoke(messages)


# 🖨️ Output
print(final.content)