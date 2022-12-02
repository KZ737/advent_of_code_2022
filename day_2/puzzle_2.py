inputfile = open("./day_2/input.txt", "r")
curSum = 0
for line in inputfile:
    curSum += [1, 2, 3][((ord(line[0])-ord("A"))+(ord(line[2])-ord("Y"))) % 3] + [0, 3, 6][ord(line[2])-ord("X")]
print(curSum)