import re
inputfile = open("./day_5/input.txt", "r")
result = ''
stacks = []
firstline = inputfile.readline()
'''
Read the first line and parse it with a regular expression.
The regexp looks for "[<letter>]" or "   " strings separated by spaces.
Create the stacks list based on the number of matches and initiate each stack with either a letter or an empty string.
'''
m = re.findall(r"(\[[A-Z]\]|   )[ \n]", firstline)
for string in m:
    if string[1] == " ":
        stacks.append("")
    else:
        stacks.append(string[1])
for line in inputfile:
    '''
    Fill up the stacks with the same regular expression as at the first line.
    '''
    m = re.findall(r"(\[[A-Z]\]|   )[ \n]", line)
    if not m:
        '''
        If we find a line that doesn't match our regexp, then the starting stack description is over, so we break from the loop.
        '''
        break
    for i, string in enumerate(m):
        if string[1] != " ":
            stacks[i] += string[1]
'''
Reverse the stack strings so that the topmost element will be the last in the string.
'''
for i in range(len(stacks)):
    stacks[i] = stacks[i][::-1]
'''
Parse the remaining lines with a regular expression looking for "move <number> from <number> to <number>".
Get the last numOfMoves characters of the string at moveFrom and append them to the string at moveTo, then remove the substring from moveFrom.
'''
for line in inputfile:
    m = re.match("move ([0-9]+) from ([0-9]+) to ([0-9]+)", line)
    if m:
        numOfMoves, moveFrom, moveTo = map(int, m.groups())
        moveFrom, moveTo = moveFrom-1, moveTo-1
        movedString = stacks[moveFrom][len(stacks[moveFrom])-numOfMoves:]
        stacks[moveTo] += movedString
        stacks[moveFrom] = stacks[moveFrom][:len(stacks[moveFrom])-numOfMoves]
'''
Go over all stacks and add the last elements to our result string.
'''
for stack in stacks:
    result += stack[-1]
print(result)
inputfile.close()