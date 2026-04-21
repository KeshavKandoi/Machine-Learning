from langgraph.graph import StateGraph, MessagesState, START, END
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict


load_dotenv() 

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class LLM_State(TypedDict):
   question:str
   answer:str

def solving(state:LLM_State)->LLM_State:
   
   question=state["question"]

   prompt=f'Answer the following question{question}'

   answer=model.invoke(prompt).content

   return {"question": question, "answer": answer}


  

graph=StateGraph(LLM_State)


graph.add_node("solving",solving)

graph.add_edge(START, "solving")
graph.add_edge("solving", END)

workflow = graph.compile()


initial_state={'question':'how far is the moon from the earth'}

final_state=workflow.invoke(initial_state)
print(final_state)
