
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore



pdf_path = Path(__file__).parent/"nodejs.pdf"

loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)

split_docs = text_splitter.split_documents(documents=docs)


print(len(docs))

print(len(split_docs))

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
    output_dimensionality=768,
    api_key="AIzaSyAYDJbAiGZpGbr1rGKvItvcFrrIVpJzEmE"
)

# vector_store = QdrantVectorStore.from_documents(
#   documents=[],
#     embedding=embeddings,
#     collection_name="my_documents",
#     url="http://localhost:6333",
# )

# vector_store.add_documents(documents=split_docs)
# print("Injection done")



retriever=QdrantVectorStore.from_existing_collection(

    embedding=embeddings,
    collection_name="my_documents",
    url="http://localhost:6333",
)

search_result=retriever.similarity_search(
  query="what is fs module"
)

print("relevant chunk",search_result)

SYSTEM_PROMPt=f"""
you are a helpful ai assistant which solves all the problem

context:{search_result}
"""