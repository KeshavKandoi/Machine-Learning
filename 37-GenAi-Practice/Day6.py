from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv() 

question=input("enter the text-:")

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt=[(
  "system","You are a helpful assistant  that solve the problem"),
  ("user", "{question}")
  ]

chain=prompt|model

response = chain.invoke({"question": question})

print(response.content)