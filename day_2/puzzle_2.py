inputfile = open("./day_2/input.txt", "r")
curSum = 0
for line in inputfile:
    '''
    1, 2, or 3 points to the winner, the principle is the same as in the first puzzle of today, just reversed:
        we add the result (-1, 0, and 1 for lose, draw, and win, respectively) to the value of the shape chosen by our opponent to get the value of our shape (mod 3)
    0, 3, or 6 points for the outcome, which is determined only by the second letter
    '''
    curSum += [1, 2, 3][((ord(line[0])-ord("A"))+(ord(line[2])-ord("Y"))) % 3] + [0, 3, 6][ord(line[2])-ord("X")]
print(curSum)
inputfile.close()