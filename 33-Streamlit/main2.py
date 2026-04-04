import streamlit as st

st.title("Chai Maker App")

if st.button("Make Chai"):
  st.success("Your chai has been brewed successfully!")

add_masala=st.checkbox("Add Masala")

if add_masala:
  st.write("Masala added to your chai")

tea_type=st.radio("Pick your chai base:",["Milk","Water","Lemon"])

st.write(f"Selected chai base: {tea_type}")

flavour=st.selectbox("Choose your chai flavour:",["Adarak","Elaichi","Tulsi","Ginger","Lemon"])

st.write(f"Selected chai flavour: {flavour}")



sugar=st.slider("Select sugar level:",0,50,23)

st.write(f"selected sugar level:{sugar} grams")

cups=st.number_input("how many cups",min_value=1,max_value=100 ,step=5)
st.write(f"Number of cups: {cups}")

name=st.text_input("Enter your name:")
if name:
  st.write(f"Welcome, {name}! Your chai is being prepared.")


dob=st.date_input("Enter your date of birth:")
st.write(f"Your date of birth is: {dob}")