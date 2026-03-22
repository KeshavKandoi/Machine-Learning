from langchain_community.document_loaders import CSVLoader

loader=CSVLoader(file_path='DD.csv')

docs=loader.load()

print("********************************************")

print(len(docs))

print("********************************************")


print(docs[0])


print("********************************************")


print(docs[4])
print("********************************************")