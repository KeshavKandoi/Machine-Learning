from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt=PromptTemplate(
  template='write a summary for the following poem-\n{poem}',
  input_variable=['poem']

)

parser=StrOutputParser()

loader=TextLoader('cricket.txt',encoding='utf-8')

docs=loader.load()

print(type(docs))

print(len(docs))

print(docs[0].page_content)


print("********************************************")

print(docs[0].metadata)

print("********************************************")

chain=prompt|model|parser

print(chain.invoke({'poem':docs[0].page_content}))


