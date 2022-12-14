import numpy as np
inputfile = open("./day_14/input.txt", "r")

'''
Import rock data from the input, discarding duplicates.
'''
rockData = []
for line in inputfile:
    data = [list(map(int, coords.split(","))) for coords in line.strip().split(" -> ")]
    if data not in rockData:
        rockData.append(data)

'''
Set the starting point, then iterate over all vertices of rocks to find the bounding box of the cave.
The bottom of the cave is 2 units below the lowest rock.
'''
startingPoint = [500, 0]
bounds = [startingPoint.copy(), startingPoint.copy()]
for rock in rockData:
    for vertex in rock:
        bounds[0][0] = min(bounds[0][0], vertex[0])
        bounds[0][1] = min(bounds[0][1], vertex[1])
        bounds[1][0] = max(bounds[1][0], vertex[0])
        bounds[1][1] = max(bounds[1][1], vertex[1])
bounds[1][1] += 2

'''
We need at least the same width (centered on the starting point) to the cave as the height for the full triangle to be able to form, so we expand the bounding box accordingly.
After that, we normalize the starting point to the new bounding box.
'''
height = bounds[1][1] - bounds[0][1]
if height > (startingPoint[0]-bounds[0][0]):
    bounds[0][0] -= (height - (startingPoint[0] - bounds[0][0]))
if height > (bounds[1][0] - startingPoint[0]):
    bounds[1][0] += (height - (bounds[1][0] - startingPoint[0]))
startingPoint = [startingPoint[0] - bounds[0][0], startingPoint[1] - bounds[0][1]]

'''
Create the map of the cave with full of 0s initially (air).
Then iterate over all rocks and fill the ones given in the input (normalized by the bounds) with 1s.
Unfortunately the indexing of matrix elements is done in the reverse order compared to the coordinate view (i.e. the "elevation" (the row number) is the first index), so we have to use them in reverse order.
'''
caveMap = np.zeros((bounds[1][1]-bounds[0][1]+1, bounds[1][0]-bounds[0][0]+1), dtype=np.byte)
for rock in rockData:
    startVertex = rock[0]
    for vertex in rock[1:]:
        rockStart = [min(startVertex[0]-bounds[0][0], vertex[0]-bounds[0][0]), min(startVertex[1]-bounds[0][1], vertex[1]-bounds[0][1])]
        rockEnd = [max(startVertex[0]-bounds[0][0], vertex[0]-bounds[0][0]), max(startVertex[1]-bounds[0][1], vertex[1]-bounds[0][1])]
        caveMap[rockStart[1]:rockEnd[1]+1,rockStart[0]:rockEnd[0]+1] = 1
        startVertex = vertex

'''
After normalizing everything else, we normalize the bounds themselves, then fill the bottommost row with rocks.
'''
bounds = [[0, 0], [bounds[1][0]-bounds[0][0], bounds[1][1] - bounds[0][1]]]
caveMap[bounds[1][1], :] = 1

'''
The grains of sand will be represented by 2s on the map.
'''
class Sand:
    def __init__(self, startCoords, caveMap):
        self.coords = startCoords
        caveMap[self.coords[1], self.coords[0]] = 2

    '''
    Moves the grain of sand to a new coordinate. Commented lines only work in Python 3.11 or above.
    '''
    def move(self, newCoords, caveMap):
        # caveMap[*list(reversed(self.coords))] = 0
        caveMap[self.coords[1], self.coords[0]] = 0
        self.coords = newCoords
        caveMap[self.coords[1], self.coords[0]] = 2
        # caveMap[*list(reversed(self.coords))] = 2
        
    '''
    Returns: 0 if sand fell into a new place but not the abyss, 1 if it stopped, 2 if fell into the abyss.
    If the grain of sand is at the bottom of our map, it will fall into the abyss, so the function returns 2.
    If the grain of sand is not at the bottom of the map, we check if it can go down by one. If it can, it will do so, and return 0.
    If the grain of sand cannot move down, we check if it's at the left side of the map. If it is, it falls into the abyss and returns 2.
    If the grain of sand is not at the left side of the map, we check if it can move diagonally left. If it can, it will do so, and return 0.
    If the grain of sand cannot move diagonally left, we check if it's at the right side of the map. If it is, it falls into the abyss and returns 2.
    If the grain of sand is not at the right side of the map, we check if it can move diagonally right. If it can, it will do so, and return 0.
    If the grain of sand cannot move diagonally right, it means that it has settled, so the function returns 1.
    '''
    def fallOneStep(self, caveMap, bounds):
        if self.coords[1] == bounds[1][1]:
            return 2
        if caveMap[self.coords[1]+1, self.coords[0]] == 0:
            self.move([self.coords[0], self.coords[1]+1], caveMap)
            return 0
        if self.coords[0] > bounds[0][0]:
            if caveMap[self.coords[1]+1, self.coords[0]-1] == 0:
                self.move([self.coords[0]-1, self.coords[1]+1], caveMap)
                return 0        
            if self.coords[0] < bounds[1][0]:
                if caveMap[self.coords[1]+1, self.coords[0]+1] == 0:
                    self.move([self.coords[0]+1, self.coords[1]+1], caveMap)
                    return 0
                else:
                    return 1
        return 2
    
    '''
    Simulates the grain of sand falling while it can.
    If the result of falling one step is that the grain of sand moved (fallOneStep returns 0), it continues to try moving again.
    If the result of falling one step is that the grain of send has settled or that it has fallen into the abyss, return 1 or 2, respectively.
    '''
    def fallUntilStopped(self, caveMap, bounds):
        while True:
            fallResult = self.fallOneStep(caveMap, bounds)
            if fallResult == 0:
                continue
            else:
                return fallResult

'''
We start with 0 grains of sand, then we create one, let it fall while it can.
If the grain of sand, after falling, has a y coordinate of 0, we are finished and we break from the loop.
If the grain of sand does not have a y coordinate of 0, we create another one and let that one fall as well, and repeat.
'''
sandCount = 0
while True:
    sandCount += 1
    newSand = Sand(startingPoint, caveMap)
    stopped = newSand.fallUntilStopped(caveMap, bounds)
    if newSand.coords[1] == 0:
        break
    else:
        continue

print(sandCount)

inputfile.close()

'''
Writes a drawing of the cave to a file. Sand is yellow, rocks are brown, and air is blue.
'''
def drawing(byte):
    if byte == 2:
        return "🟨"
    elif byte == 1:
        return "🟫"
    else:
        return "🟦"

outputfile = open("./day_14/output.txt", "w", encoding="utf-8")
np.set_printoptions(threshold=np.inf)
outputfile.write(np.array2string(caveMap, max_line_width=np.inf, separator='', formatter={"int": drawing}))
outputfile.close()