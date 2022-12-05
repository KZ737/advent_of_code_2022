inputfile = open("./day_3/input.txt", "r")
curSum = 0
sacks = []
for line in inputfile:
    '''
    Get every triplet of lines into sets and get their intersection to get the common element. 
    After we have 3 sacks, which we simply calculate the priority of the common element, then reset the sacks.
    '''
    sacks.append(set(list(line.strip())))
    if len(sacks) == 3:
        commonElement = sacks[0].intersection(sacks[1]).intersection(sacks[2]).pop()
        curSum += (ord(commonElement) - ord("a") + 1) if commonElement.islower() else (ord(commonElement) - ord("A") + 27)
        sacks = []
print(curSum)
inputfile.close()