# pip install beautifulsoup4

import os
os.environ["USER_AGENT"] = "Mozilla/5.0 ..."


from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt=PromptTemplate(
  template='Answer the following questions \n {questions} from the following text - \n{text}',
  input_variable=['questions','text']

)

parser=StrOutputParser()


url="https://en.wikipedia.org/wiki/Cricket"

loader=WebBaseLoader(url)


docs=loader.load()

answer=input("you : ")

chain=prompt|model|parser

result=chain.invoke({'questions':'answer','text':docs[0].page_content})


print(result)