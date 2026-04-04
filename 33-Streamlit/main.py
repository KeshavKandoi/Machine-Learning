import streamlit as st

st.title("Hello, Streamlit!")
st.subheader("This is a simple Streamlit app.")
st.text("You can use Streamlit to create interactive web applications with Python.")
st.write("Here's an example of a simple Streamlit app that displays some text and a button.")


chai=st.selectbox("Your Fav chai:",["Masala chai","Adrak chai","Green tea","Lemon tea","Black tea","Coffee","Cold coffee"])

st.write(f" your choice {chai} is very good")


st.success("Your chai has been brewed successfully!")