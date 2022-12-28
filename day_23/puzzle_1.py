import numpy as np
inputfile = open("./day_23/input.txt", "r")

'''
Read the input into a list, then build a numpy array, and find the coordinates of the elves.
'''
elves = []
for line in inputfile:
    elves.append(list(line.strip()))
elves = np.array(elves)
elves = [tuple(elf) for elf in np.argwhere(elves == "#")]

'''
N, NE, E, SE, S, SW, W, NW
'''
def neighbours(elf):
    return [(elf[0]-1, elf[1]), (elf[0]-1, elf[1]+1), (elf[0], elf[1]+1), (elf[0]+1, elf[1]+1), (elf[0]+1, elf[1]), (elf[0]+1, elf[1]-1), (elf[0], elf[1]-1), (elf[0]-1, elf[1]-1)]

'''
The directions, the corresponding neighbours, and the moves in those directions.
'''
directions = ["N", "S", "W", "E"]
directionNeighbours = {"N": [0, 1, 7], "S": [3, 4, 5], "W": [5, 6, 7], "E": [1, 2, 3]}
directionMoves = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}

'''
The function makes all elves take one step. The directions list is updated to the new order.
First we define a dictionary of the proposed moves: the keys are the new locations and the values are the location(s) from where an elf (or some elves) would step from.
The updateProposedMoves function takes a new location and an old location, and updates the proposedMoves accordingly: if there are no elves wanting to step there, we create a new item, else we append to the item's already existing value.
'''
def step(elves, directions):
    proposedMoves = {}
    def updateProposedMoves(newElf, elf):
        if newElf not in proposedMoves.keys():
            proposedMoves.update({newElf: [elf]})
        else:
            proposedMoves[newElf].append(elf)

    '''
    First half: getting all the proposed locations.
    We iterate over all elves, and for each elf, we do the following:
        1. If there are no elves in any of its neighbouring 8 cells, it stays in place (i.e. the proposed move is staying in place).
        2. We iterate over all directions, and if there are no elves in a given direction, we propose a move there, and do not continue our search in other directions.
        3. If we haven't proposed any move yet, we stay in place.
    We move the first checked direction to the last place.
    '''
    for elf in elves:
        elfNeighbours = neighbours(elf)

        for neighbour in elfNeighbours:
            if neighbour in elves:
                break
        else:
            newElf = elf
            updateProposedMoves(newElf, elf)
            continue
        
        for direction in directions:
            dirNeighbours = [elfNeighbours[i] for i in directionNeighbours[direction]]
            for dirNeighbour in dirNeighbours:
                if dirNeighbour in elves:
                    break
            else:
                newElf = (elf[0]+directionMoves[direction][0], elf[1]+directionMoves[direction][1])
                updateProposedMoves(newElf, elf)
                break
        else:
            newElf = elf
            updateProposedMoves(newElf, elf)
    
    directions = directions[1:] + [directions[0]]
        
    '''
    Second half: moving.
    The finalElves list will contain all the new positions of the elves.
    We iterate over all points whereto a move is proposed, and check if there is only 1 elf wanting to move there.
    If this is the case, we add the proposed point to the list of new positions.
    If there are more elves wanting to move there, we add all the elves initial positions to the finalElves list, since all of them stays in place.
    '''
    finalElves = []
    for proposedEndPoint, proposedStartingPoints in proposedMoves.items():
        if len(proposedStartingPoints) == 1:
            finalElves.append(proposedEndPoint)
        else:
            for elf in proposedStartingPoints:
                finalElves.append(elf)
    return finalElves, directions

'''
Helper function used for debugging.
Turns the elves' locations into a 2D numpy array, then prints it.
'''
def printElfMap(elves):
    minX, maxX, minY, maxY = [min([elf[1] for elf in elves]), max([elf[1] for elf in elves]), min([elf[0] for elf in elves]), max([elf[0] for elf in elves])]
    elfMap = np.full(((maxY-minY+1), (maxX-minX+1)), fill_value=".")
    for elf in elves:
        elfMap[(elf[0]-minY, elf[1]-minX)] = "#"
    elfMap = np.array2string(elfMap, max_line_width=np.inf, separator='', formatter={"str_kind": lambda x: x})
    print(elfMap)

'''
We have the elves take 10 steps.
'''
for i in range(10):
    elves, directions = step(elves, directions)

'''
The number of free spots can be calculated by multiplying the difference of the extrema on both axes, and subtracting the number of elves from this value.
'''
minX, maxX, minY, maxY = [min([elf[1] for elf in elves]), max([elf[1] for elf in elves]), min([elf[0] for elf in elves]), max([elf[0] for elf in elves])]
print((maxX-minX+1)*(maxY-minY+1) - len(elves))

inputfile.close()