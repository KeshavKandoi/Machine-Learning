class car:
  def __init__(self,brand,model):
    self.brand=brand
    self.model=model

  def full_name(self):
    return(f"{self.brand},{self.model}")

class ElectricCar(car):
    def __init__(self,brand,model,battery):
      super().__init__(brand,model)
      self.battery=battery

my_Tesla=ElectricCar("Tesla","Model S","90kwh")
print(my_Tesla.battery)
print(my_Tesla.full_name())

my_car=car("Toyota","corolla")

print(my_car.brand)
print(my_car.model)
print(my_car.full_name())

my_new_car=car("Tata","Nexon")
print(my_new_car.brand)