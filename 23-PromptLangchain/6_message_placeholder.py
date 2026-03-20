# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# # chat template
# chat_template = ChatPromptTemplate([
#     ('system','You are a helpful customer support agent'),
#     MessagesPlaceholder(variable_name='chat_history'),
#     ('human','{query}')
# ])

# chat_history = []
# # load chat history
# with open('chat_history.txt') as f:
#     chat_history.extend(f.readlines())

# print(chat_history)

# # create prompt
# prompt = chat_template.invoke({'chat_history':chat_history, 'query':'Where is my refund'})

# print(prompt)

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Chat template
chat_template = ChatPromptTemplate([
    ('system', 'You are a helpful customer support agent'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human', '{query}')
])

chat_history = []

# Load chat history from file
with open('chat_history.txt') as f:
    chat_history.extend(f.readlines())

print("Loaded history:", chat_history)

# Create chain
chain = chat_template | model

# Invoke with history and new query
result = chain.invoke({
    'chat_history': chat_history,
    'query': 'Where is my refund'
})

print("AI:", result.content)