inputfile = open("./day_9/input.txt", "r")

'''
We have a positions list, containing the positions of the knots.
The 0th is the head, and we have 9 following it, the 9th one being the tail.
We once again have a set for the coordinates visited by the tail.
'''
length = 10
positions = [[0, 0] for i in range(length)]
visited = set()

'''
For each input line, we move the head.
Then we move each knot according to its placement compared to the one before it, see puzzle_1.py for the 2 basic moves.
There is one new potential relative placement: since knots 1-9 can move diagonally (unlike the head), the situation where one element is 2 units away from the previous element _in both directions_, in which case we move diagonally but neither of the coordinates will be the same as the previous element's.
'''
for line in inputfile:
    direction, steps = line.strip().split()
    steps = int(steps)
    for i in range(steps):
        match direction:
            case "U":
                positions[0][1] += 1
            case "D":
                positions[0][1] -= 1
            case "R":
                positions[0][0] += 1
            case "L":
                positions[0][0] -= 1
        for j in range(1, length):
            if abs(positions[j-1][0] - positions[j][0]) >= 2 and abs(positions[j-1][1] - positions[j][1]) >= 2:
                positions[j] = [((positions[j-1][0] + positions[j][0]) // 2), ((positions[j-1][1] + positions[j][1]) // 2)]
            elif abs(positions[j-1][0] - positions[j][0]) >= 2:
                positions[j] = [((positions[j-1][0] + positions[j][0]) // 2), positions[j-1][1]]
            elif abs(positions[j-1][1] - positions[j][1]) >= 2:
                positions[j] = [positions[j-1][0], ((positions[j-1][1] + positions[j][1]) // 2)]
        visited.add(tuple(positions[length-1]))

print(len(visited))

inputfile.close()