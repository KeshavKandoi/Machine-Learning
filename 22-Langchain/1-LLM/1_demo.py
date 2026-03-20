from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
     model='gemini-2.5-flash',
)

result = llm.invoke("What is the capital of India?")

print(result.content)


# from langchain_openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# llm=OpenAI(model='gpt-3.5-turbo-instruct')

# result=llm.invoke("what is the capital of india")

# print(result)