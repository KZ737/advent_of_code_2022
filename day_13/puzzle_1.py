inputfile = open("./day_13/input.txt", "r")

'''
If the first number is smaller, then return 1 ("good order"), if the second is smaller, return -1 ("bad order"), if they are equal, return 0 ("undecided")
'''
def compareInts(int1: int, int2: int):
    if int1 < int2:
        return 1
    elif int2 < int1:
        return -1
    else:
        return 0

'''
Compare the elements of the lists pairwise, return 1 or -1 on the first occassion they are different. If they are all the same, decide based on length.
'''
def compareLists(list1: list, list2: list):
    itemnums = min(len(list1), len(list2))
    for idx in range(itemnums):
        valpair = compare(list1[idx], list2[idx])
        if valpair == 1:
            return 1
        elif valpair == -1:
            return -1
    if len(list1) < len(list2):
        return 1
    elif len(list2) < len(list1):
        return -1
    else:
        return 0

'''
If both are numbers, compare with the integer function, if both are lists, compare them as lists, if one of them is a number and the other is a list, convert the number to a list and compare as such.
'''
def compare(left, right):
    if type(left) == int and type(right) == int:
        return compareInts(left, right)
    elif type(left) == list and type(right) == list:
        return compareLists(left, right)
    elif type(left) == list and type(right) == int:
        return compareLists(left, [right])
    else:
        return compareLists([left], right)

input = inputfile.read()
input = input.strip().split("\n\n")

sumOfIdx = 0

'''
For each pair of packets we compare them, and if they are in a good order, add the index to the sum of indices.
'''
for packetIdx, packetPair in enumerate(input, 1):
    packet1, packet2 = map(eval, map(str.strip, packetPair.split("\n")))
    if compare(packet1, packet2) == 1:
        sumOfIdx += packetIdx

print(sumOfIdx)

inputfile.close()