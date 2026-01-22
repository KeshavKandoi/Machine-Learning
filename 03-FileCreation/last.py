

data=True
line=1

with open("xx.txt","r") as f:
 while data:
  data=f.readline()
  if("bihar"in data):
   print(f"word found at{line}")
   break
  line=line+1
  print(data)

# ✅ The correct truth (VERY IMPORTANT)
# 🔹 There are TWO different things:
# What it is	Value	Boolean value
# Blank line	"\n"	True
# End of file (EOF)	""	False