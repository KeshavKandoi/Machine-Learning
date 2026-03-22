from langchain_community.document_loaders import PyPDFLoader

loader=PyPDFLoader('Transformer.pdf')

docs=loader.load()

print(docs)

print("********************************************")

print(len(docs))

print("********************************************")

print(docs[0].page_content)

print("********************************************")


print(docs[1].metadata)