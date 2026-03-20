# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import streamlit as st

# load_dotenv()
# model=ChatOpenAI()

# st.header('Research Tool')

# user_input=st.text_input("enter your prompt")

# if st.button('Summarize'):
#   result=model.invoke(user_input)
#   st.write(result.content)




# run code---  streamlit run Static_prompt.py  



from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

st.header('Research Tool')

user_input = st.text_input("Enter your prompt")

if st.button('Summarize'):
    if user_input.strip():
        result = model.invoke(user_input)
        st.write(result.content)
    else:
        st.warning("Please enter a prompt first.")