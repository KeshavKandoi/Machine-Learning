from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

llm= ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# Checkpointer
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

# using streaming 

#  for adding  stream 


# for message_chuck,meatadata in chatbot.stream( 
#     {'message':[HumanMessage(content='what is the recipe to make pasta')]},
#     config={"configurable":{'thread_id':'thread-1'}},
#     stream_mode='messages'
# ):
#     if message_chuck.content:
#         print(message_chuck.content,end=" ",flush=True)