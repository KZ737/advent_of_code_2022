inputfile = open("./day_10/input.txt", "r")

'''
X starts at 0, and when the computer starts executing, we're already at cycle 1.
The sum of strength is originally 0.
'''
X = 1
cycle = 1
sumOfStrengths = 0

for line in inputfile:
    '''
    If we are in the 20th, 60th, etc. cycle, add cycle*X to the sum of strengths.
    '''
    if (cycle % 40) == 20:
        sumOfStrengths += cycle * X
    command = line.strip().split()
    '''
    If the command is addx, then see if the next cycle would be the 20th, 60th, etc., and act accordingly.
    Then add the given number to X, and 2 to the cycle counter.
    If the command is not addx (e.g. it's noop), just increase cycle number by 1.
    '''
    if command[0] == "addx":
        if ((cycle + 1) % 40) == 20:
            sumOfStrengths += (cycle + 1) * X
        X += int(command[1])
        cycle += 2
    else:
        cycle += 1

print(sumOfStrengths)

inputfile.close()