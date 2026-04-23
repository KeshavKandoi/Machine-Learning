from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.checkpoint.memory import InMemorySaver 
from typing_extensions import TypedDict
import requests
import json
import datetime
from langchain_ollama import ChatOllama

load_dotenv()

checkpointer = InMemorySaver()

model1 = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

model2 = ChatOllama(model="qwen:7b")



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


llm_with_tools = model1.bind_tools(tools)


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


workflow1 = graph.compile()



class parentClass(TypedDict):
   question: str
   research: str    # filled by Agent 1
   report: str

def research(state:parentClass)->parentClass:
   question=state["question"]
   prompt1=f"research about the question {question} and give the description"
   response=workflow1.invoke(
       {"messages": [{"role": "user", "content": prompt1}]}
  )
   last = response["messages"][-1].content
   if isinstance(last, list):
        research_text = last[0]["text"]
   else:
        research_text = last
   

   return {"research":research_text}


def report(state:parentClass)->parentClass:
   research=state["research"]
   prompt2 = f"Give a 5 bullet point report in ENGLISH ONLY about:\n{research}"

   report=model2.invoke(prompt2).content
   return{"report":report}


graph = StateGraph(parentClass)

graph.add_node("research",research)
graph.add_node("report",report)

graph.add_edge(START, "research")
graph.add_edge("research","report")
graph.add_edge("report",END)


workflow2 = graph.compile(checkpointer=checkpointer)





while True:

  prompt=input("enter your message-:")

  result = workflow2.invoke(
           
           {"question":prompt},
          {"configurable": {"thread_id": "1"}},
  )

  answer = result["report"]
  print(answer)

  approval = input("Save this answer? (yes/no): ")

  if approval.lower() == "yes":
   log_data = {
      "thread_id": "1",
      "question": prompt,
      "answer": answer,
      "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


   with open("research_log.json", "a") as f:
      json.dump(log_data, f)
      f.write("\n")   

  else:
      print("skipped — not saved.")




   