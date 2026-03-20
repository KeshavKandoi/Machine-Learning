
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")  

documents=["delhi is the capital of india",
           "jaipur is the capital of rajasthan",
           "Bengaluru is the capital of karnataka"]

result = embedding.embed_documents(documents)

print(str(result))