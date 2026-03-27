# run 
#  uvicorn main:app --reload     

from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def hello():
  return {'message':'Hello world'}

@app.get("/about")
def about():
  return {'message':"HE is the best "}