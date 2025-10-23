from os import name

from pygame import color


class carmaker:
    def __init__(self, name,  color,  year):
        self.name = name
        self.color = color
        self.year = year
        self.miles = 0
        

    def drive(self,miles):
      self.miles += miles


    def carstatus(self):
        print(self.name, self.color, self.year, self.miles)

car1 =  carmaker("hudson's car", "green", 2000)


print("1=================\n")
print(car1.name)
print("2====================\n")
car1.carstatus()
car1.drive(100)

car1.carstatus()


