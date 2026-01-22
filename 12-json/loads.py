import json

json_str='{"name": "keshav","age":  25}'
# print(type(json_str))
py_object=json.loads(json_str)
print(type(py_object))