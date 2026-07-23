from pydantic import BaseModel

class Student(BaseModel):


  name:str


new_student={'name':'nitish'}

student=Student(**new_student)


print(student)

""" 

What is Pydantic?

Pydantic is a Python library that checks whether the data we receive is correct or not. It also converts data into the correct type if possible.

It is mainly used with FastAPI to validate request data.

Why do we use Pydantic?

We use Pydantic to:

Check if the input data is valid.
Convert data types automatically (like "21" to 21).
Prevent invalid data from entering our application.
Reduce the amount of manual validation code.


The ** operator unpacks a dictionary into keyword arguments. So Student(**new_student) is equivalent to Student(name="nitish"). It's commonly used to pass dictionary data directly to functions or Pydantic models.

"""