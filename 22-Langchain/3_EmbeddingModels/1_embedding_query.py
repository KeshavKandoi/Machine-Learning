# from langchain_openai import OpenAIEmbeddings
# from dotenv import load_dotenv

# load_dotenv()

# embedding=OpenAIEmbeddings(model='text-embedding-3-large',dimensions=32)

# result=embedding.embed_query("Delhi is the capital of india")


# print(str(result))




from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")  

result = embedding.embed_query("Delhi is the capital of india")

print(str(result))