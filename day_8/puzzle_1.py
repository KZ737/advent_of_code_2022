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
All trees on the edge are visible.
'''
visible = 4 * (len(trees)-1)

'''
If a tree is taller than any* on its left, right, up, or down, it is visible.
*this is equivalent to the given tree being taller than the tallest tree in the given direction
'''
for i in range(1, len(trees)-1):
    for j in range(1, len(trees)-1):
        if max(trees[i,:j]) < trees[i,j] or max(trees[i,j+1:]) < trees[i,j] or max(trees[:i,j]) < trees[i,j] or max(trees[i+1:,j]) < trees[i,j]:
            visible += 1

print(visible)

inputfile.close()