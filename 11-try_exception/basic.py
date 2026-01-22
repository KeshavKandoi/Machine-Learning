try:
     x=int(input("enter the number:"))
     ans=10/x

except ZeroDivisionError:
    print("divide by zero is not possible")

else:
  print(f"ans={ans}")

finally:
    print("end of the program")




