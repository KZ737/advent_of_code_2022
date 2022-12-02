inputfile = open("./day_1/input.txt", "r")
sums = []
curSum = 0
for line in inputfile:
    if line != "\n":
        curSum += int(line)
    else:
        sums.append(curSum)
        curSum = 0
sums.sort(reverse=True)
print(sums[0], sum(sums[0:3]))