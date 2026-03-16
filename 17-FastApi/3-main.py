from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse
from typing import Annotated,Literal,Optional
import json

app=FastAPI()

class Patient(BaseModel):

  id:Annotated[str,Field(...,description='ID of the pateint',examples=['P001'])]
  name:Annotated[str,Field(...,description='Name of the patient')]
  city:Annotated[str,Field(...,description='city where the patient is living')]
  age:Annotated[int,Field(...,gt=0,lt=120,description='Age of  the pateint')]
  gender:Annotated[Literal['male','female','other'],Field(...,description='Gender of the pateint')]
  height:Annotated[float,Field(...,gt=0,description='Height of the pateint in meter')]
  weight:Annotated[float,Field(...,gt=0,description='Weight of the pateint in kgs')]

 
  @computed_field
  @property
  def bmi(self)->float:
      bmi=round(self.weight/(self.height**2),2)
      return bmi

  @computed_field
  @property
  def verdict(self)->str:
      if self.bmi<18.5:
         return 'underweight'
      elif self.bmi<25:
         return 'Normal'
      elif self.bmi<30:
         return 'Overweight'
      else:
         return 'obese'
      

class PatientUpdate(BaseModel):
   name:Annotated[Optional[str],Field(default=None)]
   city:Annotated[Optional[str],Field(default=None)]
   age:Annotated[Optional[int],Field(default=None,gt=0)]
   gender:Annotated[Optional[Literal['male','female','other']],Field(default=None)]
   height:Annotated[Optional[float],Field(default=None,gt=0)]
   weight:Annotated[Optional[float],Field(default=None,gt=0)]
         

def load_data():
  with open('patients4.json','r') as f:
    data=json.load(f)


  return data

def save_data(data):
   with open('patients4.json','w') as f:
      json.dump(data,f)


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
def view_patient(patient_id:str=Path(...,description="ID of the patient in the DB",example="P001")):
  data=load_data()

  for patient in data["patients"]:
    if patient["patient_id"] == patient_id:
       return patient

  raise HTTPException(status_code=404,detail="Patient not found")



@app.get("/sort")
def sort_patients(sort_by:str=Query(...,description='Sort on the basic of height,weight or bmi'),order:str=Query('asc',description='sort in asc or desc order')):

  valid_fields=['height','weight','bmi']

  if sort_by not in valid_fields:
    raise HTTPException(status_code=400,detail=f"Invalid field select from {valid_fields}")
  

  if order not in ['asc','desc']:
    raise HTTPException(status_code=400,detail="Invalid order select between asc and desc")

  
  data=load_data()

  sort_order= True if order=='desc' else False

  sorted_data=sorted(data["patients"],key=lambda x:x.get(sort_by,0),reverse=sort_order)

  return sorted_data
    


@app.post("/create")
def create_patient(patient: Patient):

    data = load_data()

    # check if patient already exists
    for p in data["patients"]:
        if p["id"] == patient.id:
            raise HTTPException(status_code=400, detail="Patient already exists")

    data["patients"].append(patient.model_dump())

    save_data(data)

    return {"message": "Patient created successfully"}


@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    patient_found = None

    for patient in data["patients"]:
        if patient["id"] == patient_id:
            patient_found = patient
            break

    if patient_found is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    updated_data = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        patient_found[key] = value

    patient_obj = Patient(**patient_found)

    updated_patient = patient_obj.model_dump()

    patient_found.update(updated_patient)

    save_data(data)

    return {"message": "Patient updated successfully"}

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):

    data = load_data()

    patient_found = None

    for patient in data["patients"]:
        if patient["id"] == patient_id:
            patient_found = patient
            break

    if patient_found is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    data["patients"].remove(patient_found)

    save_data(data)

    return {"message": "Patient deleted successfully"}
