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
        operations.update({m.group("ID"): m.group("op").replace("/", "//")})

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

'''
We print the value of the variable named "root".
Note: "print(root)" has exactly the same result, but most editors highlight that, as they think that variable "root" is undefined. This eval is there for purely (editor-)cosmetic reasons.
'''
print(eval("root"))

inputfile.close()