import functools
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
    if type(left) == list and type(right) == list:
        return compareLists(left, right)
    elif type(left) == int and type(right) == int:
        return compareInts(left, right)
    elif type(left) == list and type(right) == int:
        return compareLists(left, [right])
    else:
        return compareLists([left], right)

input = inputfile.read()
input = input.strip().split("\n")
while "" in input:
    input.remove("")

'''
Sort using the compare function. Since I wrote my compare function in a reverse manner compared to how Python understands them by default (the return value should be negative if the first item is smaller, and vice versa), we sort in the "reverse order".
Then look for the indices of [[2]] and [[6]], add 1 to them (because the packets are numbered with 1-based indexing), then multiply them together.
'''
packets = []
for packet in input:
    packets.append(eval(packet))
packets.append([[2]])
packets.append([[6]])
packets.sort(key=functools.cmp_to_key(compare), reverse=True)
print((packets.index([[2]]) + 1) * (packets.index([[6]]) + 1))

inputfile.close()