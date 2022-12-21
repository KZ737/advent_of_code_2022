'''
!!!!!!!
UNSAFE SOLUTION: you should _NEVER_ use exec() on an unsanitized input.
!!!!!!!

This was the first solution that came to my mind and first I thought "I guess this will work for the sample, but it will be too slow for the real input", then tried it, and, surprisingly enough, it ran under 0.05 seconds, so I didn't care to make a less awful solution.
Please, do _not_ see this as a "clever" solution, for it is a stupidly unsafe one.
'''

import re
inputfile = open("./day_21/input.txt", "r")

'''
We look for 4 letters followed by a comma, then either a number, or two 4-letter words with an operation between them.
'''
pattern = "(?P<ID>[a-z]{4}): (?:(?P<op>[a-z]{4} [-+*\/] [a-z]{4})|(?P<num>[0-9]+))"

'''
If we find a number, we execute a command equating the 4-letter word to that number. If we find an operation, we save that for later.
'''
operations = {}
for line in inputfile:
    m = re.search(pattern, line)
    if m.group("num"):
        exec(m.group("ID") + " = " + m.group("num"))
    else:
        operations.update({m.group("ID"): m.group("op")})
del pattern, line, m

'''
Now, here comes the funny part...
We make "humn" equal to the imaginary unit i (or in Python, j). This will stand as our unknown variable. By the end comparison, it will be greatly transformed by multiple equations combined, but the important thing is that there will be no other complex numbers, so there will not happen an i*i multiplication (and there are no operations that would rotate our variables in the complex plane), so this value will just take any multiplications and divisions we do with it until we get to root.
We also record which 2 variables should be equal in root's comparison, then delete that from the list of operations.
'''
humn = complex(0, 1)
root = operations["root"].split(" ")[::2]
operations.pop("root")

'''
In a loop, we try to execute all operations. If we can, we remove it from the list of operations. If we can't, we let it go and try again in the next loop. We do this until the list of operations is empty.
'''
while len(operations) > 0:
    removeList = []
    for ID, operation in operations.items():
        try:
            exec(ID + " = " + operation)
            removeList.append(ID)
        except:
            pass
    for ID in removeList:
        operations.pop(ID)
    del removeList

'''
Now, we should have arrived at 2 numbers, one of which is a usual real number, but the other is a complex one.
Let's say that the first is the complex one, and will be represented as such: x = a + b*i; while the second number is y.
Since i is "equal" to the number we are looking for, we have a very simple equation to solve:
y = a + b*i
The solution is obviously i = (y - a) / b.
Since we do not know beforehand which variable is the complex and which is the real, we just make them both complex, and our solution will change as such: x = a + b*i; y = c + d*i; where either b or d is 0.
a + b*i = c + d*i
i = (c - a) / (b - d)
Of course since we had fractions before, this number will be a float, but should be very close to an integer.
So we print exactly that.
'''
rootLeft = complex(eval(root[0]))
rootRight = complex(eval(root[1]))
print(int((rootRight.real - rootLeft.real) / (rootLeft.imag - rootRight.imag)))

inputfile.close()