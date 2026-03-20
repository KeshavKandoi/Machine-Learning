from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint

from dotenv import load_dotenv

load_dotenv()

llm=HuggingFaceEndpoint(
     repo_id="Qwen/Qwen2.5-72B-Instruct", 
    task="text-generation"
)

model=ChatHuggingFace(llm=llm)


result=model.invoke("what is the capital of Russia")


print(result.content)