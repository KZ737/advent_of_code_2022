import numpy as np
import re
inputfile = open("./day_22/input.txt", "r")

'''
The lines read until an empty line will constitute the map of the grove.
We replace all spaces with Ts, which will are short for "teleportation", i.e. edges where if we would step on them, we would be teleported.
We record the maximum length of the lines for padding purposes later.
'''
groveMap = []
maxLength = 0
while (line := inputfile.readline()) != "\n":
    groveLine = line.rstrip().replace(" ", "T")
    maxLength = max(maxLength, len(groveLine))
    groveMap.append(groveLine)

'''
We insert a line full of Ts to the front and to the end of the map.
We also pad all lines so that the first and last columns are also full of Ts.
'''
groveMap.insert(0, ''.join(["T" for _ in range(maxLength)]))
groveMap.append(''.join(["T" for _ in range(maxLength)]))
for idx in range(len(groveMap)):
    groveMap[idx] = groveMap[idx].ljust(maxLength+1, "T")
for idx in range(len(groveMap)):
    groveMap[idx] = list(groveMap[idx].rjust(maxLength+2, "T"))

'''
We turn the map into a numpy array for (imo) better-looking indexing purposes.
We also make a copy for a version that shows our path too.
'''
groveMap = np.array(groveMap)
groveMapAnnotated = groveMap.copy()

'''
We read the instructions using splitting with regular expressions.
'''
instructions = inputfile.readline().strip()
pattern = "([RL])"
instructionList = [int(instruction) if instruction.isdigit() else instruction for instruction in re.split(pattern, instructions)]

'''
We set our starting point to the first "." in the groveMap array (searching by row).
We also set our initial heading to right.
'''
curPoint = np.argwhere(groveMap == ".")[0]
heading = 0
headingNames = ["R", "D", "L", "U"] # 0 for right, 1 for down, 2 for left, 3 for up
headingDirections = [(0, 1), (1, 0), (0, -1), (-1, 0)]
arrows = [">", "v", "<", "^"]

'''
Move function.
First calculates the new coordinates. If there is a "#" there, we break because we can't move.
If there's a "T" there, we walk in the other direction until we find another "T", then step one back and continue. (If there happens to be a "#" just after the other "T", we stay in place and do not teleport.)
'''
def move(startPoint, steps, heading, groveMap):
    coords = startPoint
    for _ in range(steps):
        newCoords = [coords[0] + headingDirections[heading][0], coords[1] + headingDirections[heading][1]]
        if groveMap[newCoords[0], newCoords[1]] == "#":
            break
        if groveMap[newCoords[0], newCoords[1]] == "T":
            newCoords = [newCoords[0] - headingDirections[heading][0], newCoords[1] - headingDirections[heading][1]]
            while groveMap[newCoords[0], newCoords[1]] != "T":
                newCoords = [newCoords[0] - headingDirections[heading][0], newCoords[1] - headingDirections[heading][1]]
            newCoords = [newCoords[0] + headingDirections[heading][0], newCoords[1] + headingDirections[heading][1]]
            if groveMap[newCoords[0], newCoords[1]] == "#":
                break
            groveMapAnnotated[newCoords[0], newCoords[1]] = arrows[heading]
            coords = newCoords
            continue
        groveMapAnnotated[newCoords[0], newCoords[1]] = arrows[heading]
        coords = newCoords
    return coords

'''
If the turning direction is "R", we step in our list up one, else we step down one.
'''
def turn(curHeading, turnDirection):
    return (curHeading+1)%4 if turnDirection == "R" else (curHeading-1)%4

'''
We iterate through the list of instructions, if we find a number, we take that amount of steps in our current heading, else we turn in the corresponding direction.
'''
for instruction in instructionList:
    if type(instruction) == int:
        curPoint = move(curPoint, instruction, heading, groveMap)
    else:
        heading = turn(heading, instruction)

'''
Calculate our result: the row number * 1000, the column number * 4, and the heading. (Note that we do not need to subtract 1, because thanks to the padding, the rows and columns are already indexed from 1.)
'''
print((curPoint[0])*1000 + (curPoint[1])*4 + heading)

inputfile.close()

'''
Helper function for the visualization: we replace the Ts with spaces for sake of clarity.
'''
def drawing(byte):
    if byte == "T":
        return " "
    else:
        return byte

'''
Set an E for the ending point in the visualization, so that we can find it quickly.
Print the visualization into a file.
'''
groveMapAnnotated[curPoint[0], curPoint[1]] = "E"
outfile = open("./day_22/output.txt", "w")
np.set_printoptions(threshold=np.inf)
outfile.write(np.array2string(groveMapAnnotated, max_line_width=np.inf, separator='', formatter={"str_kind": drawing}))
outfile.close()