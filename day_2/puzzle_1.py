inputfile = open("./day_2/input.txt", "r")
curSum = 0
for line in inputfile:
    curSum += [1, 2, 3][ord(line[2])-ord("X")] + [3, 6, 0][ord(line[2])-ord(line[0])-ord("X")+ord("A")]
print(curSum)