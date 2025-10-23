


array_1 = [1,1,1,1,1]
array_2 = [2,2,2,2,2]
array_3 = [3,3,3,3]

ar1len = len(array_1)
ar2len = len(array_2)
ar3len = len(array_3)



def FindShortArray(*arrays):
    return min(arrays, key=len)


Shortest = FindShortArray(array_1, array_2, array_3)




def FindShortArray(*arrays):
    return max(arrays, key=len)


Longest = FindShortArray(array_1, array_2, array_3)



ShortestArray = (len(Shortest))
LongestArray = (len(Longest))

for i in range(ShortestArray):
    print(array_2[i] - array_1[i] + array_3[i])


if ShortestArray != LongestArray:
    print("no index value")
