from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.checkpoint.memory import InMemorySaver  
import requests
import json
import datetime

load_dotenv()

checkpointer = InMemorySaver()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")



@tool
def search_tool(query: str) -> str:
    """Search the web"""
    search = DuckDuckGoSearchRun()
    return search.invoke(query)



@tool
def get_stock_price(symbol: str) -> str:
    """Get stock price like AAPL, TSLA"""
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=YOUR_API_KEY"
    r = requests.get(url)
    return str(r.json())



tools = [search_tool, get_stock_price]


llm_with_tools = model.bind_tools(tools)


tool_node = ToolNode(tools)



def llm_node(state: MessagesState):
    system = {"role": "system", "content": "You have access to full conversation history. Use it to answer questions about previous messages."}
    messages = [system] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


graph = StateGraph(MessagesState)

graph.add_node("llm", llm_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "llm")


graph.add_conditional_edges("llm", tools_condition)


graph.add_edge("tools", "llm")


workflow = graph.compile(checkpointer=checkpointer)

while True:

  prompt=input("enter your message-:")

  result = workflow.invoke({
      "messages": [
          {"role": "user", "content": prompt}]}
          ,{"configurable": {"thread_id": "1"}},
  )

  last = result["messages"][-1].content
  if isinstance(last, list):
    answer = last[0]["text"]
  else:
    answer = last

  print(answer)

 
  log_data = {
      "thread_id": "1",
      "question": prompt,
      "answer": answer,
      "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  }


  with open("research_log.json", "a") as f:
      json.dump(log_data, f)
      f.write("\n")   



