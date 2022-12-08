import numpy as np

inputfile = open("./day_8/input.txt", "r")

'''
Read all the lines into a list of lists, then convert that to a numpy 2D array.
'''
trees = []
for line in inputfile:
    trees.append(list(map(int, list(line.strip()))))
trees = np.array(trees)

'''
Helper function, returns a list of arrays containing the height of trees in the 4 directions.
'''
def directions(array, i, j):
    return [array[i,:j][::-1], array[i,j+1:], array[:i,j][::-1], array[i+1:,j]]

'''
We use numpy.where to look for trees higher or of the same height than a given tree.
If no such trees are found in a given direction (i.e. numpy.where()[0] has 0 length), all trees are visible so we use the length of the array, i.e. the number of trees in the direction.
If there are trees fulfilling the condition, we take the index of the first one, and add 1 to it (e.g. if we can only see the first tree in one direction, that will have an index of 0).
We do this for all 4 directions, then multiply these distances together to calculate the scenic score, the maximum of which we are looking for.
'''
maxScore = 0
for i in range(1, len(trees)-1):
    for j in range(1, len(trees)-1):
        distances = [np.where(direction >= trees[i,j])[0][0]+1 if len(np.where(direction >= trees[i,j])[0]) != 0 else len(direction) for direction in directions(trees, i, j)]
        scenicScore = np.prod(distances)
        maxScore = max(maxScore, scenicScore)

print(maxScore)

inputfile.close()