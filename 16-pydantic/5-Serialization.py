from pydantic import BaseModel,EmailStr,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):

  # name:str=Field(max_length=50)

  name:Annotated[str,Field(max_length=50,title='Name of the pateint',description='Give the name of the patient in less than 50 characters',examples=['Nitish','Amit'])]
  email:EmailStr
  age:int
  weight:float=Field(gt=0,lt=100)
  height:float
  married:Optional[bool]=None
  allergies:List[str]
  contact_details:Dict[str,str]


  @computed_field
  @property
  def calculate_bmi(self)->float:
    bmi=round(self.weight/(self.height**2),2)
    return bmi

def insert_patient_data(patient:Patient):

  print(patient.name) 
  print(patient.age)
  print(patient.email)
  print(patient.weight)
  print(patient.married)   
  print(patient.allergies)
  print(patient.height)
  print(patient.calculate_bmi)
  print(patient.contact_details)
  print('inserted')


patient_info={'name':'nitish','email':'kk@hdfc.com','age':90,'weight':76.3,'height':1.72,'married':True,'allergies':['pollen','dust'],'contact_details':{'emergency':'12345678','phone':'2323333432'}}

patient1=Patient(**patient_info)


insert_patient_data(patient1)


# temp=patient1.model_dump()

# print(temp)
# print(type(temp))
# dict k liye


temp=patient1.model_dump.json()

print(temp)
print(type(temp))

# json k liye
