import numpy as np
inputfile = open("./day_12/input.txt", "r")

'''
We define an elevation map by the ASCII value of the letters.
We turn that list[list[int]] into a numpy ndarray object for easier further use.
We look for the starting and ending points, and change their elevations to the starting and ending elevations, respectively.
We also retrieve the longitudinal and latitudinal size of the map.
'''
elevationMap = []
for line in inputfile:
    elevationMap.append(list(map(ord, list(line.strip()))))
elevationMap = np.array(elevationMap)
elevationMap[np.where(elevationMap == ord("S"))] = ord("a")
endCoord = np.where(elevationMap == ord("E"))
endCoord = tuple([endCoord[0][0], endCoord[1][0]])
elevationMap[endCoord] = ord("z")
width, height = elevationMap.shape

'''
We define a distance function which returns 1 if one can traverse from node1 to node2, i.e. node2's height is at most node1's height + 1. If this is not the case, it returns infinity.
'''
def distance(elevMap, node1: int, node2: int):
    return 1 if elevMap[node2] - elevMap[node1] <= 1 else np.inf

'''
We define a function that returns all viable neighbours of a node. We check against the sizes of the map so that we don't run out of bounds.
'''
def neighbours(xcoord: int, ycoord: int, height: int, width: int):
    neigh = []
    for x, y in [(xcoord-1, ycoord), (xcoord+1, ycoord), (xcoord, ycoord-1), (xcoord, ycoord+1)]:
        if (0 <= x < width) and (0 <= y < height):
            neigh.append((x, y))
    return neigh

'''
Breadth-first search: we start at all points with the lowest elevation, i.e. elevation "a".
We enqueue all viable neighbours (along with their distances, that are the distance of the current point +1) that have not been visited yet, then go over the queue and add their neighbours as well, etc.
In each loop we check if we arrived at the ending point, and if we did, we print the distance traversed, and break the loop.
'''
lowestElevations = np.where(elevationMap == ord("a"))
lowestElevations = [tuple([lowestElevations[0][i], lowestElevations[1][i]]) for i in range(len(lowestElevations[0]))]
visited = set(lowestElevations)
queue = [(0, startCoord) for startCoord in lowestElevations]
while queue:
    dist, node = queue.pop(0)
    if node == endCoord:
        print(dist)
        break
    for neighNode in neighbours(node[0], node[1], height, width):
        if (distance(elevationMap, node, neighNode) == 1) and (neighNode not in visited):
            visited.add(neighNode)
            queue.append((dist+1, neighNode))

inputfile.close()