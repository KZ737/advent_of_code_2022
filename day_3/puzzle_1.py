inputfile = open("./day_3/input.txt", "r")
curSum = 0
for line in inputfile:
    '''
    Get both halves of the line into sets and get their intersection to get the common element.
    After which we simply calculate the priority of the common element.
    '''
    sacks = [set(list(line.strip()[:len(line)//2])), set(list(line.strip()[len(line)//2:]))]
    commonElement = sacks[0].intersection(sacks[1]).pop()
    curSum += (ord(commonElement) - ord("a") + 1) if commonElement.islower() else (ord(commonElement) - ord("A") + 27)
print(curSum)
inputfile.close()