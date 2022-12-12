import re
import math
inputfile = open("./day_11/input.txt", "r")

'''
A monkey has an initial assortment of items, the operation it's doing to the worry level, an integer against which the divisibility it checks, and 2 monkeys to which it throws the items depending on the value of the check.
A monkey can be given an item through addItem(), which appends an item to its items list.
In inspecAndThrow(), a monkey goes through all items in its list, performs the operation on its worry level, calculates its remainder against the least common multiple (see later), checks against the divisibility with testInt, then gives that item to the corresponding monkey. It also increases its inspectedItems value by one.
'''
class Monkey:
    def __init__(self, startingItems: list[int], operation, testInt: int, trueMonkey: int, falseMonkey: int):
        self.items = startingItems
        self.operation = operation
        self.testInt = testInt
        self.trueMonkey = trueMonkey
        self.falseMonkey = falseMonkey
        self.inspectedItems = 0

    def addItem(self, item: int):
        self.items.append(item)

    def inspectAndThrow(self, monkeys: list, lcm: int):
        while self.items:
            item = self.items.pop()
            item = self.operation(item)
            item %= lcm
            if item % self.testInt == 0:
                monkeys[self.trueMonkey].addItem(item)
            else:
                monkeys[self.falseMonkey].addItem(item)
            self.inspectedItems += 1

'''
See comment in puzzle_1.py on line 55 for purpose.
'''
def createOp(string):
    return lambda old: eval(string)

'''
We break the input up every time there are two newlines after each other, then look for the regex pattern in each part. The pattern retrieves the monkey's id, initial assortment of items, worry level operation, divisibility test integer, and the monkeys it can throw items to.
'''
pattern = "Monkey (?P<id>[0-9]+):\n\s+Starting items: (?P<startingItems>[0-9, ]+)\n\s+Operation: new = (?P<op>[-+*\/old 1-9]+)\n\s+Test: divisible by (?P<testInt>[0-9]+)\n\s+If true: throw to monkey (?P<trueMonkey>[0-9]+)\n\s+If false: throw to monkey (?P<falseMonkey>[0-9]+)"

input = inputfile.read()
input = input.split("\n\n")

monkeys = {}

for monkey in input:
    m = re.match(pattern, monkey)
    id, testInt, trueMonkey, falseMonkey = map(int, [m.group("id"), m.group("testInt"), m.group("trueMonkey"), m.group("falseMonkey")])
    startingItems = list(map(int, m.group("startingItems").split(",")))
    operation = createOp(m.group("op"))
    newMonkey = Monkey(startingItems, operation, testInt, trueMonkey, falseMonkey)
    monkeys.update({id: newMonkey})

'''
Since we are not dividing the worry level by 3 each time, the worry levels would increase exponentially at some monkeys. To combat this, we calculate the least common multiple of the divisibility test integers of the monkeys. After every inspection, we take the remainder against this number, since it will not change the remainder against any of the test integers. (Kind of similarly to the Chinese Remainder Theorem.)
'''
monkeysLCM = math.lcm(*[monkey.testInt for monkey in monkeys.values()])

'''
We simulate the monkeys inspecting and throwing their items for 10000 rounds.
'''
for round in range(10000):
    for monkeyId in sorted(monkeys):
        monkeys[monkeyId].inspectAndThrow(monkeys, monkeysLCM)

'''
We sort the monkeys list by the number of inspected items, and multiply the first two values.
'''
print(math.prod(monkey.inspectedItems for monkey in sorted(monkeys.values(), key = lambda monkey: monkey.inspectedItems, reverse = True)[:2]))

inputfile.close()