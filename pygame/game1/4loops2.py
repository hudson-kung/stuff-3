

names = ["tom" , "jim", "john", "hudson", "dom" ,"sarah"]
count = 15
starDown = count - 1

for i in range(count):
    print("|" * i)
    if i + 1 == count:
        for j in range(count - 1, 0, -1):
            print("|" * j)



