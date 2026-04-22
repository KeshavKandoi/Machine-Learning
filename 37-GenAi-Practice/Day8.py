from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import requests

load_dotenv()


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
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}



graph = StateGraph(MessagesState)

graph.add_node("llm", llm_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "llm")


graph.add_conditional_edges("llm", tools_condition)


graph.add_edge("tools", "llm")

workflow = graph.compile()



result = workflow.invoke({
    "messages": [
        {"role": "user", "content": "what is the stock price of apple"}
    ]
})

print(result["messages"][-1].content)