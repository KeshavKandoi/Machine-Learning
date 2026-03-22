# Lengthbase + documentLoader


from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader=PyPDFLoader("java.pdf")

docs=loader.load()


splitter=CharacterTextSplitter(
  chunk_size=100,
  chunk_overlap=0,
  separator=''
)

result=splitter.split_documents(docs)

print(result)

print("**********************************************")

print(result[0])

print("**********************************************")

print(result[0].page_content)