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


print("\nAI Agent Ready (type 'quit' to exit)\n")

while True:
   query=input("\nEnter the question:-\n")

   if query.lower()=="quit":
      print("BYEE")
      break 
   
   decision_prompt=f"""Decide:
If the question needs document search, say ONLY "SEARCH"
Otherwise say ONLY "DIRECT"

Question: {query}
"""
   
   decision=ollama.chat(model="qwen:7b",messages=[
     {
       "role":"user",
       "content":decision_prompt
     }
   ])

   decision_text=decision["message"]["content"].strip().upper()
   print(decision_text)


   if "SEARCH" in decision_text:
     
     print("\n🔍 Using RAG...\n")
     
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
     
   else:
     print("\n🧠 Direct Answer...\n")
     prompt = query
   
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