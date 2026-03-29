# by using Basetool

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

# Input schema

class MultiplyInput(BaseModel):
    a: int = Field(..., description="First number")
    b: int = Field(..., description="Second number")

# Tool class

class MultiplyTool(BaseTool):
    name: str = "multiply"
    description: str = "Multiply two numbers"
    args_schema: Type[BaseModel] = MultiplyInput  

    def _run(self, a: int, b: int):
        return a * b


tool = MultiplyTool()
result = tool.invoke({"a": 3, "b": 4})
print(result)