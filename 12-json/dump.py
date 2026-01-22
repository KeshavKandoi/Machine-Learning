import json

data= {"name":"Helllo","Type":"Hero"}

with open("python.txt","w") as f:
  py_obj=json.dump(data,f,indent=4,sort_keys=True)
  print(data)