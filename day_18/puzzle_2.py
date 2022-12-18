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
We define a function that returns all viable (not out of bounds) neighbours of a coordinate.
'''
def neighbours(coords, bounds):
    neigh = []
    for x, y, z in [(coords[0]-1, coords[1], coords[2]), (coords[0]+1, coords[1], coords[2]), (coords[0], coords[1]-1, coords[2]), (coords[0], coords[1]+1, coords[2]), (coords[0], coords[1], coords[2]-1), (coords[0], coords[1], coords[2]+1)]:
        if (0 <= x <= bounds[0]+1) and (0 <= y <= bounds[1]+1) and (0 <= z <= bounds[2]+1):
            neigh.append((x, y, z))
    return neigh

'''
Breadth-first search: we start at (0, 0, 0).
We enqueue all viable neighbours that have not been visited yet and are air (not lava), then go over the queue and add their neighbours as well, etc.
This goes on until the queue is empty, i.e. we have visited all coordinates that are reachable from (0, 0, 0), i.e. all coordinates that are outside of the lava droplets and are not contained within the lava.
'''
startPoint = (0, 0, 0)
S = [startPoint]
visited = set()
visited.add(startPoint)
while S:
    voxel = S.pop(0)
    for neighbour in neighbours(voxel, sizes):
        if neighbour not in visited and lavaDroplets[neighbour] == 0:
            visited.add(neighbour)
            S.append(neighbour)

'''
We iterate over all coordinates and if at a coordinate there is lava, we look through all its neighbours and if a neighbour has been visited by our BFS earlier (i.e. that neighbour is a cube of air _and_ is outside of the lava droplets), then we count that as one faces touching outside air. The sum of all these faces is exactly the number we are looking for.
'''
sum = 0
for i in range(1, lavaDroplets.shape[0]-1):
    for j in range(1, lavaDroplets.shape[1]-1):
        for k in range(1, lavaDroplets.shape[2]-1):
            if lavaDroplets[i, j, k] == 1:
                for neighbour in neighbours((i, j, k), sizes):
                    if neighbour in visited:
                        sum += 1

print(sum)

inputfile.close()

quit()

'''
Cool interactive 3D visualization for the lava droplets. To use, uncomment the quit() above.
Matplotlib uses CPU rendering so this is pretty slow. One alternative is provided below, which uses PlotOptiX for a much better looking result, using ray tracing.
'''
import matplotlib.pyplot as plt

ax = plt.figure().add_subplot(projection='3d')
ax.voxels(lavaDroplets, facecolors = "#DD000088", edgecolor = "#33333388", linewidth=0.5)
plt.show()

'''
from plotoptix import TkOptiX
from plotoptix.materials import m_plastic

plot = TkOptiX()
plot.set_param(min_accumulation_step=10, max_accumulation_frames=10000, light_shading="Soft")
xyz = [[i, j, k] for i in range(1, lavaDroplets.shape[0]-1) for j in range(1, lavaDroplets.shape[1]-1) for k in range(1, lavaDroplets.shape[2]-1) if lavaDroplets[i, j, k] == 1]
plot.set_background(0.99)
plot.setup_material("plastic", m_plastic)
plot.show()
plot.update_camera(eye=[-15, -15, -15], target = [20, 20, 20])
plot.setup_light("Sun", pos=[20, 150, 20], color=[9, 9, 7], radius=15)
plot.set_data("Lava droplets", xyz, u=[1,0,0], v=[0,1,0], w=[0,0,1], geom="Parallelepipeds", mat="plastic", c = (1.5, 0, 0))
'''