#imports

from enum import unique
from os import popen

#list functions

''' def lists():
    numbers = [3,1,4]
    print(numbers)
    numbers.append(1)
    print(numbers)
    numbers.insert(3,10)
    print(numbers)
    numbers.remove(3)
    print(numbers)
    # pop = numbers.pop()
    # print(pop)
    numbers.sort()
    numbers.reverse()
    print(numbers)

    multiplied = [2 * number for number in numbers]
    print(multiplied)

lists() '''

#quizlists

'''def quizLists():

    list = []
    list.append(1)
    print(list)
    list.append(3)
    print(list)
    list.insert(1,2)
    print(list)
    list.remove(3)
    print(list)
    listX5 = [n * 5 for n in list]
    print(listX5)'''

#tuples

'''quizLists()

tuple = ("blue", "red")
blue, red = tuple
print(red, blue)'''

#how to make a dictionary

'''location = {
    "Run": "To move at a speed faster than walking by taking quick steps in which each foot is lifted before the next foot touches the ground.",
    "Jump": "To push oneself off the ground and into the air using the muscles in one's legs and feet.",
    "Walk": "To move at a regular pace by lifting and setting down each foot in turn, never having both feet off the ground at once.",
    "Jog": "To run at a steady, gentle pace, typically for physical exercise.",
    "Sleep": "A natural and periodic state of rest during which consciousness of the world is suspended and the body's metabolic processes are slowed down."
}'''

#unique values

rawdata =  [1,1,2,2,3,3,4,4,5,5]
unique = {item for item in rawdata}
# print(unique)









'''car = {"color": "red", "make": "bmw", "year": 2024}
#print(car["make"])
print("Favorite color:", car.get("color","unknown"))'''



inventory = {
    "fruits": [
        {
            "name": "apple",
            "quantity": 100
        },
        {
            "name": "orange",
            "quantity": 100
        }
    ],
    "vegetables": [
        {
            "name": "carrot",
            "quantity": 50
        }
    ]   
}





for item in inventory["vegetables"]:
    if item["name"] == "carrot":
        item["quantity"] += 50

print(inventory)

