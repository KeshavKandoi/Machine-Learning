from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated,Literal

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from langchain.tools import tool
import requests


load_dotenv()

llm= ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


class IdentitySchema(BaseModel):
  value:Literal["Math","Generator","Stock"]=Field(description="value must be from this only")

structured_model1=llm.with_structured_output(IdentitySchema)





class IdentityState(TypedDict):
  question:str
  value:str
  essay: str
  score: int
  attempts: int
  ans: str 
  price: float     
  action: str 


def Classifier(State:IdentityState)->IdentityState:

  question=State["question"]

  prompt=f""" classify this question into one of these categories Math, Generator, Stock: {State['question']}"""

  value=structured_model1.invoke(prompt).value
  return {
        **State,
        "value": value
    }





class EssaySchema(BaseModel):
    score: int = Field(
        ge=0,
        le=10,
        description="Score must be between 0 and 10"
    )
    essay:str=Field(description="Generate essay on the given topic")

structured_model2=llm.with_structured_output(EssaySchema)


class MathState(TypedDict):
  question:str
  ans:str
  value:str


def Calculation(state:IdentityState)->IdentityState:

  question=state["question"]

  prompt=f""" solve this {state['question']} math problem and give the answer only without Explanation:

  """

  ans=llm.invoke(prompt).content
  
  return {
        **state,   
        "ans": ans
    }


class GeneratorState(TypedDict):
  question:str
  essay:str
  score:int
  value: str



def Generator(state: IdentityState) -> IdentityState:

    question = state["question"]

    prompt = f"""write an essay on this topic {question}"""

    result = structured_model2.invoke(prompt)

    return {
        **state,
        "essay": result.essay,
        "score": result.score,
        "attempts": state.get("attempts", 0)
    }

def Evaluator(state: IdentityState) -> IdentityState:

    score = state["score"]

    return {
        **state,
        "attempts": state.get("attempts", 0) + 1
    }

def check_score(state):
    if state["score"] >= 5:
        return "done"
    elif state["attempts"] >= 5:
        return "done"
    else:
        return "retry"
    



class StockState(TypedDict):
  question:str
  value:str


@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=EPDZ3L9OQ71FGG1T"
    r = requests.get(url)
    return r.json()

   
def Stock_Fetch(state: IdentityState) -> IdentityState:
    
    question = state["question"]
    
    symbol = llm.invoke(
      f"Extract stock ticker symbol from: {question}"
      ).content.strip().upper()

    data = get_stock_price.invoke({"symbol": symbol})

    try:
        price = float(data["Global Quote"]["05. price"])
    except:
        price = 0

    return {
        **state,
        "price": price
    }
def Stock_Decision(state: IdentityState) -> IdentityState:

    price = state["price"]

    if price < 200:
        action = "BUY STOCK"
    else:
        action = "DO NOT BUY"

    return {
        **state,
        "action": action,
        "ans": f"Price: {price}, Action: {action}"
    }
def route(state):
    return state["value"]




graph=StateGraph(IdentityState)

graph.add_node("Classifier", Classifier)
graph.add_node("Calculation", Calculation)
graph.add_node("Generator", Generator)
graph.add_node("Evaluator", Evaluator)
graph.add_node("Stock_Fetch", Stock_Fetch)
graph.add_node("Stock_Decision", Stock_Decision)




graph.add_edge(START, "Classifier")    
graph.add_conditional_edges(
    "Classifier",
    route,
    {
        "Math": "Calculation",
        "Generator": "Generator",
        "Stock":"Stock_Fetch" 
    }
)

graph.add_edge("Calculation", END)
graph.add_edge("Stock_Fetch", "Stock_Decision")
graph.add_edge("Stock_Decision", END)

graph.add_edge("Generator", "Evaluator")
graph.add_conditional_edges(
    "Evaluator",
    check_score,
    {
        "retry": "Generator",
        "done": END
    }
)




workflow = graph.compile()

# result = workflow.invoke({"question": "what is the price of Nvidia"})
result = workflow.invoke({"question":  " solve 6+6/12"})  
# result = workflow.invoke({"question":  " write an essay 33"}) 
print(result)





