from pydantic import BaseModel,EmailStr,Field,field_validator
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):

  # name:str=Field(max_length=50)

  name:Annotated[str,Field(max_length=50,title='Name of the pateint',description='Give the name of the patient in less than 50 characters',examples=['Nitish','Amit'])]
  email:EmailStr
  age:int
  weight:float=Field(gt=0,lt=100)
  married:Optional[bool]=None
  allergies:List[str]
  contact_details:Dict[str,str]

def insert_patient_data(patient:Patient):

  print(patient.name) 
  print(patient.age)
  print(patient.weight)
  print(patient.married)   
  print(patient.allergies)
  print(patient.contact_details)
  print('inserted')


patient_info={'name':'nitish','email':'kk@gmail.com','age':30,'weight':76.3,'married':True,'allergies':['pollen','dust'],'contact_details':{'email':'abc@gmail.com','phone':'2323333432'}}

patient1=Patient(**patient_info)


insert_patient_data(patient1)