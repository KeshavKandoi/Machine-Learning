class car:
  def __init__(self,brand,model):
    self.__brand=brand
    self.model=model
# __ se private ho jata hai

  def get_brand(self):
   return self.__brand + " ! " 

  def full_name(self):
    return(f"{self.__brand},{self.model}")

class ElectricCar(car):
    def __init__(self,brand,model,battery):
      super().__init__(brand,model)
      self.battery=battery

my_Tesla=ElectricCar("Tesla","Model S","90kwh")
print(my_Tesla.battery)
print(my_Tesla.get_brand())
#print(my_Tesla.__brand)
print(my_Tesla.full_name())
