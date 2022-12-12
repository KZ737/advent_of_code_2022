inputfile = open("./day_6/input.txt", "r")
text = inputfile.readline()
'''
Starting from the 4th character, look at a given character and the 3 preceding it, and convert them into a set (where there cannot be more than 1 element of the same value).
If the size of this set is the same as the number of letters converted into the set (4), that means they are 4 distinct characters, so we print the index of the element, then break.
'''
for i in range(4, len(text)):
    if len(set(text[i-4:i])) == 4:
        print(i)
        break
inputfile.close()