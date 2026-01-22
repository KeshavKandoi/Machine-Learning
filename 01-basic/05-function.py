def generator(limit):
  for i in range(2,limit+1,2):
    yield i
  
for j in generator(10):
    print(j)

# yield pauses the function and returns a value.

# When the loop continues, it resumes from the paused point.

# This allows multiple values to be generated one by one.