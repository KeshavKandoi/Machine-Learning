from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader

loader=DirectoryLoader(
  path='books',
  glob='*.pdf',
  loader_cls=PyPDFLoader

)

docs=loader.load()

print(len(docs))

print("********************************************")
print(docs[0].page_content)


print("********************************************")

print(docs[0].metadata)


print("********************************************")

print(docs[62].page_content)

print("********************************************")

print(docs[62].metadata)