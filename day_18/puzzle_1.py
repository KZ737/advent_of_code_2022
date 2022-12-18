import numpy as np

inputfile = open("./day_18/input.txt", "r")

'''
Read coordinates from file.
'''
coords = []
for line in inputfile:
    coords.append(list(map(int, line.strip().split(","))))

'''
Calculate the minimum coordinates and the overall extent of the lava droplets along all 3 axes.
'''
mins = [min([coord[0] for coord in coords]), min([coord[1] for coord in coords]), min([coord[2] for coord in coords])]
sizes = [max([coord[0] for coord in coords]) - min([coord[0] for coord in coords]) + 1, max([coord[1] for coord in coords]) - min([coord[1] for coord in coords]) + 1, max([coord[2] for coord in coords]) - min([coord[2] for coord in coords]) + 1]

'''
Normalize coordinates such that the minima along all axes is 1.
'''
for coord in coords:
    for i in range(3):
        coord[i] -= mins[i] - 1

'''
Create a 3D numpy array filled with 0s (denoting air) which is 2 units larger than the extent of the lava droplets, so that we have one line of 0-padding along all faces.
Then fill the array with 1s where there is lava.
'''
lavaDroplets = np.zeros((sizes[0]+2,sizes[1]+2,sizes[2]+2), dtype=np.byte)
for coord in coords:
    lavaDroplets[coord[0], coord[1], coord[2]] = 1

'''
3D convolution matrix that takes only the 6 touching faces into account.
'''
convolution = np.array([[[0, 0, 0], [0, 1, 0], [0, 0, 0]], [[0, 1, 0], [1, 0, 1], [0, 1, 0]], [[0, 0, 0], [0, 1, 0], [0, 0, 0]]])

'''
Since air is denoted by 0 and lava by 1, if we take the convolution of the 3x3x3 subarrays of the lavaDroplets with the convolution array, we should get the number of all faces touching. Unfortunately we also have to take into account that we should only calculate the elementwise product of the subarrays when they are centered on a lava block. Since I do not know of such a selective convolution function pre-written, we do this with ourselves. The sum of all these elementwise products is exactly the number of faces of cubes that are touching.
'''
sum = 0
for i in range(1, lavaDroplets.shape[0]-1):
    for j in range(1, lavaDroplets.shape[1]-1):
        for k in range(1, lavaDroplets.shape[2]-1):
            if lavaDroplets[i, j, k] == 1:
                sum += np.sum(lavaDroplets[i-1:i+2, j-1:j+2, k-1:k+2] * convolution)

'''
The overall number of lava droplets is just the sum of all elements in the 3D array (once again, because air is 0 and lava is 1), and the overall area of the cubes is 6 times this number.
Thus, the number of faces touching air are 6*number of cubes - the previously calculated sum.
'''
print(np.sum(lavaDroplets)*6 - sum)

inputfile.close()