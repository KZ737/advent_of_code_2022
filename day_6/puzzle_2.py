import re
inputfile = open("./day_6/input.txt", "r")
text = inputfile.readline()
'''
Same principle as before.
Starting from the 14th character, look at a given character and the 13 preceding it, and convert them into a set (where there cannot be more than 1 element of the same value).
If the size of this set is the same as the number of letters converted into the set (14), that means they are 14 distinct characters, so we print the index of the element, then break.
'''
for i in range(14, len(text)):
    if len(set(text[i-14:i])) == 14:
        print(i)
        break
inputfile.close()