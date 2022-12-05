inputfile = open("./day_2/input.txt", "r")
curSum = 0
for line in inputfile:
    '''
    1, 2, or 3 points for the chosen shape
    In the order of rock, paper, and scissors, each element is beaten by the next element, so if we subtract the value of our opponent's shape from ours, we get:
        0 if we chose the same shape -> draw,
        1 if I chose the one following theirs -> I win,
        -1 if I chose the one which is followed by theirs -> they win.
        
    In languages where indexing with negative numbers is not possible, a mod 3 is needed for the indexing of the second array (turning -1 into 2)
    '''
    curSum += [1, 2, 3][ord(line[2])-ord("X")] + [3, 6, 0][ord(line[2])-ord(line[0])-ord("X")+ord("A")]
print(curSum)
inputfile.close()