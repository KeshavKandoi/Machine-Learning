from langchain.tools import tool



@tool("calculator", description="Performs arithmetic calculations. Use this for any math problems.")
def calc(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))

result=calc.invoke({"expression":"2+3"})

print(result)





