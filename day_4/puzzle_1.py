inputfile = open("./day_4/input.txt", "r")
curSum = 0
for line in inputfile:
    '''
    Parse the line: split by the comma, then parse the resulting strings by splitting them by the hyphen, then mapping them to int.
    One is completely inside the other if (min1 <= min2 AND max1 => max2) or vice versa.
    '''
    sections = [list(map(int, sectionstring.split("-"))) for sectionstring in line.split(",")]
    if (sections[0][0] <= sections[1][0] and sections[0][1] >= sections[1][1]) or (sections[0][0] >= sections[1][0] and sections[0][1] <= sections[1][1]):
        curSum += 1
print(curSum)