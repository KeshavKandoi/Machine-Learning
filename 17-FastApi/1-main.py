# run 
#  uvicorn main:app --reload     

from fastapi import FastAPI,Path,HTTPException,Query
import json

app=FastAPI()

def load_data():
  with open('patients.json','r') as f:
     data=json.load(f)

  return data  

@app.get("/")
def hello():
  return {'message':'pateint management system API'}

@app.get("/about")
def about():
  return {'message':"A fully functional API to manage your pateint records "}

@app.get('/view')
def view():
  data=load_data()

  return data


@app.get("/patient/{patient_id}")
def view_patient(
  patient_id:str=Path(
    ...,
    description="ID of the patient in the DB",
    example="P001")):

  # ... (three dots) is called Ellipsis in Python.

  data=load_data()

  for patient in data["patients"]:
    if patient["patient_id"] == patient_id:
       return patient

  raise HTTPException(status_code=404,detail="Patient not found")



@app.get("/sort")
def sort_patients(
  sort_by:str=Query(...,
                    description='Sort on the basic of height,weight or bmi')
  ,order:str=Query('asc',description='sort in asc or desc order')):

  valid_fields=['height','weight','bmi']

  if sort_by not in valid_fields:
    raise HTTPException(status_code=400,detail=f"Invalid field select from {valid_fields}")
  

  if order not in ['asc','desc']:
    raise HTTPException(status_code=400,detail="Invalid order select between asc and desc")

  
  data=load_data()

  sort_order= True if order=='desc' else False

  sorted_data=sorted(data["patients"],key=lambda x:x.get(sort_by,0),reverse=sort_order)

  return sorted_data
    




# FastAPI is a modern Python web framework used to build APIs quickly and efficiently. It is built on top of Starlette and Pydantic.

# HTTPException is used to return HTTP errors like 404 Not Found or 400 Bad Request with a custom message.


"""
Ellipsis (...) in FastAPI
... (Ellipsis) means the parameter is required.
If a parameter must be provided by the client, we use ....
If a parameter is optional or has a default value, we do not use ...; instead, we provide the default value.
"""