from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
import ollama


file_path = "./Java.pdf"
loader = PyPDFLoader(file_path)

documents=loader.load()




text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)
                                 
      
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    dimensions=1024,
)                       
 

vectorstore = InMemoryVectorStore.from_documents(
    texts,
    embedding=embeddings,
)


retriever = vectorstore.as_retriever()


print("\nAnswer:\n")

while True:
   query=input("Enter the question:-\n")

   if query.lower()=="quit":
      print("BYEE")
      break 

   retrieved_documents = retriever.invoke(query)

   context="\n\n".join(
      [doc.page_content for doc in retrieved_documents]
   )

   prompt = f"""
Answer ONLY from the context below.

Context:
{context}

Question:
{query}

Give answer in points:
1 ->
2 ->
"""




   response=ollama.chat(model="qwen:7b",messages=[
  {
    "role":"user",
    "content":prompt,
  }
  ],stream=True
)

   for chunk in response:
    print(chunk["message"]["content"],end="", flush=True)