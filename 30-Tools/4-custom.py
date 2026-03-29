#  by using pydantic

from langchain_core.tools import StructuredTool
from pydantic import BaseModel,Field


class Multiplyfunction(BaseModel):
  a:int=Field(...,description="The first number to add ")
  b:int=Field(...,description="The second number to add ")
  

def multiply(a,b):
  return a*b

multiply_tool=StructuredTool.from_function(
  func=multiply,
  name='multiply',
  description="MUltiply two nuumber",
  args_schema=Multiplyfunction
)

result=multiply_tool.invoke({"a":3,"b":2})

print(result)

