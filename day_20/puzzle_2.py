'''
Doubly linked list. The move function moves the node along the chain by as many steps as its value. The function takes the length of the chain as a parameter for faster calculation.
'''
class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None
    
    def move(self, N):
        if self.value == 0:
            return
        self.prev.next = self.next
        self.next.prev = self.prev
        curNode = self
        for i in range(self.value % (N-1)):
            curNode = curNode.next
        self.next = curNode.next
        self.prev = curNode
        self.next.prev = self
        curNode.next = self

'''
For debug purposes. Prints the list from the first node of the input.
'''
def printNodesFromFirst(firstNode):
    curNode = firstNode
    nodeVals = []
    while True:
        nodeVals.append(curNode.value)
        curNode = curNode.next
        if curNode == firstNode:
            break
    print(nodeVals)

'''
For debug purposes. Prints the list from the node with 0 value.
'''
def printNodesFromZero(zeroNode):
    curNode = zeroNode
    nodeVals = []
    while True:
        nodeVals.append(curNode.value)
        curNode = curNode.next
        if curNode == zeroNode:
            break
    print(nodeVals)

'''
Calculates the coordinates. First it builds an array with all the nodes in the list in their new order, then takes the sum of the values given (again taking advantage of the modulo operator).
'''
def getCoordinates(zeroNode):
    newNumbers = []
    curNode = zeroNode
    while True:
        newNumbers.append(curNode)
        curNode = curNode.next
        if curNode == zeroNode:
            break
    sum = newNumbers[1000 % len(newNumbers)].value + newNumbers[2000 % len(newNumbers)].value + newNumbers[3000 % len(newNumbers)].value
    return sum

'''
Read the numbers. Record the first one (for linking purposes later), and the one with 0 value.
'''
inputfile = open("./day_20/input.txt", "r")
firstNum = 811589153*int(inputfile.readline().strip())
firstNode = Node(firstNum)
numbers = [firstNode]
prevNode = firstNode
for line in inputfile:
    newNode = Node(811589153*int(line.strip()))
    if newNode.value == 0:
        zeroNode = newNode
    newNode.prev = prevNode
    prevNode.next = newNode
    numbers.append(newNode)
    prevNode = newNode

'''
Linking the first and the last.
'''
numbers[0].prev = newNode
numbers[-1].next = firstNode

'''
Moving all numbers 10 times.
'''
for _ in range(10):
    for number in numbers:
        number.move(len(numbers))

print(getCoordinates(zeroNode))

inputfile.close()