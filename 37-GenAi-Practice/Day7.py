from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict,Optional,Annotated,Literal
from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun


load_dotenv() 

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


class structured_Model(BaseModel):
    sentiment: Annotated[Literal['search','direct'],Field(description="give the answr only in search and direct ")]



structured_model=model.with_structured_output(structured_Model)

class LLM_State(TypedDict):
   question:str
   sentiment:Literal["search","direct"]
   improved_question:str
   answer:str


def SearchEngine(state:LLM_State)->dict:
    improved_question=state["improved_question"]

    search_tool=DuckDuckGoSearchRun()

    answer=search_tool.invoke(improved_question)

    return{"answer":answer}



   


def check_question(state:LLM_State)->LLM_State:
   
   prompt=f"from the question check the stuructured_model of the question\n{state['question']}"

   
   sentiment = structured_model.invoke(prompt).sentiment

   return{"sentiment":sentiment}



def route_decision(state:LLM_State):
   
   sentiment=state["sentiment"]

   if sentiment=="search":
      return  "SearchEngine"
   
   else:
      return "solving"

def problem(state:LLM_State)->LLM_State:
   question=state["question"]

   prompt = f"""
Rewrite the following question in a clear, improved form.
Return ONLY the improved question.
Do NOT add explanation, examples, or extra text.

Question: {question}
"""
   
   improved_question=model.invoke(prompt).content
   return{"improved_question":improved_question}


def solving(state:LLM_State)->LLM_State:
   
   improved_question=state["improved_question"]

   prompt=f'Answer this question briefly and directly:\n{improved_question}'

   answer=model.invoke(prompt).content

   return {"answer": answer}


  

graph=StateGraph(LLM_State)


graph.add_node("solving",solving)
graph.add_node("problem",problem)
graph.add_node("check_question",check_question)
graph.add_node("SearchEngine", SearchEngine)


graph.add_edge(START, "problem")
graph.add_edge("problem","check_question")
graph.add_conditional_edges("check_question", route_decision)
graph.add_edge("SearchEngine",END)
graph.add_edge("solving",END)


workflow = graph.compile()


initial_state={'question':'how far is the moon from the earth'}

final_state=workflow.invoke(initial_state)
print(final_state)
