from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
import ollama



loader =DirectoryLoader(
  path='book',
  glob='*.pdf',
  loader_cls=PyPDFLoader

  

)

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


retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


print("\nAnswer:\n")

while True:
   query=input("\nEnter the question:-\n")

   if query.lower()=="quit":
      print("BYEE")
      break 

   retrieved_documents = retriever.invoke(query)

   context="\n\n".join(
     [f"Source: {doc.metadata['source']}\n{doc.page_content}" 
      for doc in retrieved_documents]
   )

   prompt = f"""
Answer ONLY from the context below.

Context:
{context}

Question:
{query}

and also show the source of the pdf 

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
   print("\n")

   for chunk in response:
    print(chunk["message"]["content"],end="", flush=True)