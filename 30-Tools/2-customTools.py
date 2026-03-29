# by using @tool

from langchain.tools import tool




def multiply(a,b):
    """ MUltiply two number"""
    return a*b


def multiply(a:int,b:int)->int :
    """ MUltiply two number"""
    return a*b


@tool
def multiply(a:int,b:int)->int :
    """ MUltiply two number"""
    return a*b


result=multiply.invoke({"a":3,"b":3})

print(result)


print(multiply.name)
print(multiply.description)
print(multiply.args)