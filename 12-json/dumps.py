import json

py_object={
  "name":"keshav",
  "isStudent":True
}

json_py=json.dumps(py_object)
print(type(json_py))



# //json.dumps()
#  Python dictionary → JSON string

#  json.dump()
# //  Python dictionary → JSON file

# // json.loads()
# //  JSON string → Python dictionary

# // json.load()
# //  JSON file → Python dictionary