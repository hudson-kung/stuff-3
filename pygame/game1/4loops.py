



Names = ["Dom" , "Tim", "John", "Jane", "Bob", "Alice", "Mike", "Sally", "Tom", "Tammy"]
Ages = [5, 3, 3, 4, 4, 5, 5, 6, 6, 7]
Grades = ["A", "B", "C", "D", "E", "F", "A", "B", "C"]
Coordinates = [(1,2), (3,4), (5,6), (7,8), (9,10)]

for i in range(len(Names)):
    print(Names[i] + " " )
    for j in range(Ages[i] + 1):
        print(j)



'''for name in names:
    print("hello " + name)'''

'''for age in Ages:
    if age < 18:
        print("minor")
    else:
        print("adult")'''

'''for i in range(len(Names) - 1):
    print(Names[i] + "'s grade is " + Grades[i])''' 