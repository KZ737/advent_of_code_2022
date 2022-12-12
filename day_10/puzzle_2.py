inputfile = open("./day_10/input.txt", "r")
outputfile = open("./day_10/output.txt", "w")

'''
X starts at 0, and when the computer starts executing, we're already at cycle 1.
'''
X = 1
cycle = 1

for line in inputfile:
    '''
    If the sprite is at the cycle number mod 40, the pixel is on, so we write a "#".
    Else, we write a ".".
    '''
    if X-1 <= ((cycle-1) % 40) <= X+1:
        outputfile.write("#")
    else:
        outputfile.write(".")
    command = line.strip().split()
    '''
    Pretty much the same as in puzzle_1.py, if the command is addx, we check for the next cycle as well. (The difference being that in this case we are checking against the value of X, not 40.)
    We also check if we should break the line or not.
    Incrementing X and the cycle counter is the same as before.
    '''
    if command[0] == "addx":
        if (cycle+1) % 40 == 1:
            outputfile.write("\n")
        if X-1 <= (cycle % 40) <= X+1:
            outputfile.write("#")
        else:
            outputfile.write(".")
        X += int(command[1])
        cycle += 2
    else:
        cycle += 1
    '''
    Check if we should break the line or not.
    '''
    if cycle % 40 == 1:
        outputfile.write("\n")

inputfile.close()