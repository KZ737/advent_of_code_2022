inputfile = open("./day_4/input.txt", "r")
curSum = 0
for line in inputfile:
    '''
    Parse the line: split by the comma, then parse the resulting strings by splitting them by the hyphen, then mapping them to int.
    There is an overlap if the maximum of the lower section is higher than the minimum of the higher section.
    (Lower section == the section with the lower minimum; higher section == the section with the higher minimum.)
    '''
    sections = [list(map(int, sectionstring.split("-"))) for sectionstring in line.split(",")]
    sections = [min(sections, key=min), max(sections, key=min)]
    if sections[0][1] >= sections[1][0]:
        curSum += 1
print(curSum)