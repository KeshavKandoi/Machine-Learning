# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv

# load_dotenv()

# model=ChatOpenAI(model='gpt-4')

# result=model.invoke("what is the captial of india")

# print(result)


from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=1)

result = model.invoke("write a 5 line poem")

print(result.content)