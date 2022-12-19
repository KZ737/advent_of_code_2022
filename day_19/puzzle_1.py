import re
# import time

'''
Read the blueprints' data into a dict.
'''
inputfile = open("./day_19/input.txt", "r")
pattern = "Blueprint (?P<blueprintID>[0-9]+): Each ore robot costs (?P<oreRobotCost>[0-9]+) ore. Each clay robot costs (?P<clayRobotCost>[0-9]+) ore. Each obsidian robot costs (?P<obsidianRobotOreCost>[0-9]+) ore and (?P<obsidianRobotClayCost>[0-9]+) clay. Each geode robot costs (?P<geodeRobotOreCost>[0-9]+) ore and (?P<geodeRobotObsidianCost>[0-9]+) obsidian."
blueprints = {}
for line in inputfile:
    m = re.search(pattern, line)
    blueprintID, oreRobotCost, clayRobotCost, obsidianRobotOreCost, obsidianRobotClayCost, geodeRobotOreCost, geodeRobotObsidianCost = map(int, m.groups())
    blueprints.update({blueprintID: {"oreRobotCost": oreRobotCost, "clayRobotCost": clayRobotCost, "obsidianRobotOreCost": obsidianRobotOreCost, "obsidianRobotClayCost": obsidianRobotClayCost, "geodeRobotOreCost": geodeRobotOreCost, "geodeRobotObsidianCost": geodeRobotObsidianCost}})

'''
We simulate 24 minutes.
'''
maxTime = 24

'''
We extract the costs into a dict, and we calculate the maximum amount something costs from each material.
Then, we start a BFS. We see what we can do with our current materials, and add all of the possibilities to a queue, then process that queue and add all possible outcomes of those possibilities, etc.
A few simplifications have been made for the function to be faster:
    1. If we can buy a geode miner, buying it leads to the best outcome, i.e. we will not buy anything else nor wait in those cases.
    2. We cap the materials' amount. If we have a lot of a material (much more than we would need with our current production), it just adds to the state space but doesn't change the result, so we cap that, thus keeping our state space smaller.
    3. If we are in a state that we have visited before (in this timestep, or in an earlier one), we discard that, since we already know all possible continuations of that state.
After maxTime of timesteps, we look through all states in the queue (i.e. all states that are possible continuations of states in the previous minute), and take the maximum of the number of the geodes.
'''
def getMaxGeode(blueprint):
    costs = {"ore": blueprint["oreRobotCost"], "clay": blueprint["clayRobotCost"], "obsidian": [blueprint["obsidianRobotOreCost"], blueprint["obsidianRobotClayCost"]], "geode": [blueprint["geodeRobotOreCost"], blueprint["geodeRobotObsidianCost"]]}
    maxCosts = {"ore": max(costs["ore"], costs["clay"], costs["obsidian"][0], costs["geode"][0]), "clay": costs["obsidian"][1], "obsidian": costs["geode"][1]}
    startState = ((0, 0, 0, 0), (1, 0, 0, 0))
    S = [startState]
    visited = set()
    maxGeode = -1
    for i in range(maxTime):
        # startTime = time.time()
        newS = []
        while S:
            state = S.pop(0)
            if state in visited:
                continue
            visited.add(state)
            materials, robots = state
            if materials[0] >= costs["geode"][0] and materials[2] >= costs["geode"][1]:
                newMaterials = tuple(materials[i]+robots[i] for i in range(len(materials)))
                newMaterials = tuple([newMaterials[0] - costs["geode"][0], newMaterials[1], newMaterials[2] - costs["geode"][1], newMaterials[3]])
                newRobots = tuple(list(robots[:3]) + [robots[3]+1])
                newS.append((newMaterials, newRobots))
            else:
                if materials[0] >= costs["ore"] and robots[0] < maxCosts["ore"]:
                    newMaterials = tuple(materials[i]+robots[i] for i in range(len(materials)))
                    newMaterials = tuple([newMaterials[0] - costs["ore"]] + list(newMaterials[1:]))
                    newRobots = tuple([robots[0]+1] + list(robots[1:]))
                    newMaterials = tuple([min(newMaterials[0], 2*maxCosts["ore"]-newRobots[0]+2), min(newMaterials[1], 2*maxCosts["clay"]-newRobots[1]+2), min(newMaterials[2], 2*maxCosts["obsidian"]-newRobots[2]+2), newMaterials[3]])
                    newS.append((newMaterials, newRobots))
                if materials[0] >= costs["clay"] and robots[1] < maxCosts["clay"]:
                    newMaterials = tuple(materials[i]+robots[i] for i in range(len(materials)))
                    newMaterials = tuple([newMaterials[0] - costs["clay"]] + list(newMaterials[1:]))
                    newRobots = tuple([robots[0], robots[1] + 1] + list(robots[2:]))
                    newMaterials = tuple([min(newMaterials[0], 2*maxCosts["ore"]-newRobots[0]+2), min(newMaterials[1], 2*maxCosts["clay"]-newRobots[1]+2), min(newMaterials[2], 2*maxCosts["obsidian"]-newRobots[2]+2), newMaterials[3]])
                    newS.append((newMaterials, newRobots))
                if materials[0] >= costs["obsidian"][0] and materials[1] >= costs["obsidian"][1] and robots[2] < maxCosts["obsidian"]:
                    newMaterials = tuple(materials[i]+robots[i] for i in range(len(materials)))
                    newMaterials = tuple([newMaterials[0] - costs["obsidian"][0], newMaterials[1] - costs["obsidian"][1]] + list(newMaterials[2:]))
                    newRobots = tuple(list(robots[:2]) + [robots[2]+1, robots[3]])
                    newMaterials = tuple([min(newMaterials[0], 2*maxCosts["ore"]-newRobots[0]+2), min(newMaterials[1], 2*maxCosts["clay"]-newRobots[1]+2), min(newMaterials[2], 2*maxCosts["obsidian"]-newRobots[2]+2), newMaterials[3]])
                    newS.append((newMaterials, newRobots))
                newMaterials = tuple(materials[i]+robots[i] for i in range(len(materials)))
                newMaterials = tuple([min(newMaterials[0], 2*maxCosts["ore"]-robots[0]+2), min(newMaterials[1], 2*maxCosts["clay"]-robots[1]+2), min(newMaterials[2], 2*maxCosts["obsidian"]-robots[2]+2), newMaterials[3]])
                newS.append((newMaterials, robots))
        S = newS
        # print(i, time.time() - startTime)
    for state in S:
        maxGeode = max(maxGeode, state[0][3])
    return maxGeode

'''
We iterate through all blueprints and take the sum of the product of their indices with the maximum amount of geodes.
'''
sum = 0
for blueprintID, blueprint in blueprints.items():
    sum += blueprintID * getMaxGeode(blueprint)

print(sum)

inputfile.close()