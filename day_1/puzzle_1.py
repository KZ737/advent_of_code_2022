inputfile = open("./day_1/input.txt", "r")
curMax = 0
curSum = 0
for line in inputfile:
    if line != "\n":
        curSum += int(line)
    else:
        curMax = max(curMax, curSum)
        curSum = 0
print(curMax)
inputfile.close()