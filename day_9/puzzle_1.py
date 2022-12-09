inputfile = open("./day_9/input.txt", "r")

'''
We have a Head and a Tail, both starting at (0, 0) and a set for counting the coordinates visited by the tail.
'''
Hpos = [0, 0]
Tpos = [0, 0]
visited = set()

'''
For each input line, we move the head, then move the tail if it's too far from the head.
If the tail moves in a cardinal direction, it's like its coordinate in that direction becomes the average of the previous coordinate and the head's; while its coordinate in the other direction remains the same (i.e. equal to the head's).
If the tail moves diagonally, one of its coordinates will become equal to that of the head's, with the other being the average as in the previous case.
We can see that the second case is general enough to describe the first one as well, so we only have 2 formulae, one for each axis.
After moving the tail (or not), we add the new position to the set.
'''
for line in inputfile:
    direction, steps = line.strip().split()
    steps = int(steps)
    for i in range(steps):
        match direction:
            case "U":
                Hpos[1] += 1
            case "D":
                Hpos[1] -= 1
            case "R":
                Hpos[0] += 1
            case "L":
                Hpos[0] -= 1
        if abs(Hpos[0]-Tpos[0]) >= 2:
            Tpos = [((Hpos[0] + Tpos[0]) // 2), Hpos[1]]
        elif abs(Hpos[1]-Tpos[1]) >= 2:
            Tpos = [Hpos[0], ((Hpos[1] + Tpos[1]) // 2)]
        visited.add(tuple(Tpos))

'''
Since every element of a set must be unique, the length of the set is equal to the number of places the tail has visited.
'''
print(len(visited))

inputfile.close()