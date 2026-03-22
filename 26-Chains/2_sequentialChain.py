from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt1=PromptTemplate(
  template='generate a detailed report on {topic}',
  input_variables=['topic']
)

prompt2=PromptTemplate(
  template='generate a 5 pointer summary from the following text \n{text}',
  input_variables=['text']
)

parser=StrOutputParser()

chain=prompt1|model|parser|prompt2|model|parser

topic=input("enter the topic")

result=chain.invoke({'topic':'topic'})

print(result)

chain.get_graph().print_ascii()
