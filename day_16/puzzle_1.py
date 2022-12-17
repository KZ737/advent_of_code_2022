import re
import numpy as np
import functools
inputfile = open("./day_16/input.txt", "r")

'''
I was too tired to simplify the code, so it's a bit messy, I am deeply sorry for anyone who comes upon this and reads it.
We have a dict containing all the neighbouring valves of each valve (both denoted with the names of the valves).
We have a dict to convert between the valves' names and indices (in the order they appeared in the input).
We finally have a distinction between valves and "good valves": the latter are all the valves which can be useful to open, i.e. all valves with a flow rate > 0. (Valves with flow rate 0 are useless so their room is only useful for going through them but not stopping in them.) By having this distinction, we do not have to go through all valves when traversing the graph, but instead we build a weighted graph between all "good valves", with the weights naturally being the distances between them (we use a fairly inefficient O(n^3) loop to calculate these, but this has to be done once, after which the graph traversal becomes much faster). It must be noted that the starting valve AA might not be a valve with a non-zero flow rate, so we must add that to our list of "good valves" in order to be able to proceed from there.
We keep a dict and 2 lists for the "good valves".
The goodValvesIDtoIdx dict is for converting between names and the indices (again, in the order they appeared in the input).
List goodValvesIdxtoID converts from the index in the good valves to the name of the valve (i.e. lists the names of the good valves in the order they appear in the input).
And finally the list goodValves has the flow rates of the good valves  (similarly to goodValvesIdxtoID)
'''
pattern = "Valve (?P<valveID>[A-Z]{2}) has flow rate=(?P<flowRate>[0-9]+); (tunnel leads to valve|tunnels lead to valves) (?P<connectedValves>(?:[A-Z]{2}[, ]{0,2})+)"
valvesNeighbours = {}
valveIDtoIdx = {}
goodValvesIDtoIdx = {}
goodValvesIdxtoID = []
goodValves = []
for line in inputfile:
    m = re.search(pattern, line)
    valveID = m.group("valveID")
    flowRate = int(m.group("flowRate"))
    connectedValves = m.group("connectedValves").split(", ")
    valvesNeighbours.update({valveID: connectedValves})
    valveIDtoIdx.update({valveID: len(valveIDtoIdx)})
    if flowRate > 0 or valveID == "AA":
        goodValvesIdxtoID.append(valveID)
        goodValves.append(flowRate)
        goodValvesIDtoIdx.update({valveID: len(goodValvesIDtoIdx)})

'''
We fill a distances matrix with large values, then write 0 in the diagonals and 1 in the off-diagonals the indices of which denote neighbours.
'''
distances = np.full((len(valvesNeighbours), len(valvesNeighbours)), fill_value=1000000, dtype=np.int_)
for valveID, valveIdx in valveIDtoIdx.items():
    distances[valveIdx, valveIdx] = 0
    for neighbouringValve in valvesNeighbours[valveID]:
        distances[valveIdx, valveIDtoIdx[neighbouringValve]] = 1

'''
After that, we have the aforementioned O(n^3) loop to calculate all distances between each pair of valves.
'''
for i in range(len(valvesNeighbours)):
    for j in range(len(valvesNeighbours)):
        for k in range(len(valvesNeighbours)):
            distances[j, k] = min(distances[j, k], distances[j, i]+distances[i, k])

'''
Now we fill a smaller matrix with the distances of each pair of good valves.
'''
goodDistances = np.full((len(goodValvesIdxtoID), len(goodValvesIdxtoID)), fill_value=1000000, dtype=np.int_)
for index, valveID in enumerate(goodValvesIdxtoID):
    goodDistances[index] = 0
    for valve2ID in goodValvesIdxtoID[:index]+goodValvesIdxtoID[index+1:]:
        goodDistances[index, goodValvesIDtoIdx[valve2ID]] = distances[valveIDtoIdx[valveID], valveIDtoIdx[valve2ID]]

'''
We have 30 minutes, and start from valve AA.
'''
maxTime = 30
start = goodValvesIDtoIdx["AA"]

'''
I don't even know how long this would run if it didn't have the functools cache... I tried running it on my PC but stopped it after ~10 mins.
This is kind of like a recursive DFS solution, I think(?). To be honest, I'm not well-versed in the world of algorithms so I'm fairly unsure of the classification.
The search function has the current valve's (good) index, a list of the open valves, and the remaining time left as arguments, and returns the most amount of steam we can let out in the remaining time left. Originally I used a list for the keeping of open valves, but unfortunately that was not compatible with the functools cache thingy, so I replaced it with a tuple containing 0s and 1s for the closed and open valves, respectively. This tuple is initially full of 0s and its size is the number of good valves.
If there is no time left, it returns 0.
If we have time left and the current valve is open, it was useless to stop in this room in the first place, so we return 0.
If we have time left and the current valve is not open, we iterate over all closed valves and check how much it's worth going there, using itself. We do this twice for each closed valve: one is going after opening the valve where we're currently at (thus adding to the released pressure but taking another 1 minute of time), and one is going there immediately without opening the valve in the current room (this does not add to the released pressure but takes 1 minute less).
'''
@functools.lru_cache(maxsize=None)
def search(currentValve, openValves, timeLeft):
    if timeLeft <= 0:
        return 0
    if not openValves[currentValve]:
        maxPressureReleased = 0
        stillClosedValves = np.where(np.array(openValves) == 0)[0]
        stillClosedValves = np.delete(stillClosedValves, np.argwhere(stillClosedValves == currentValve))
        for valve in stillClosedValves:
            distance = goodDistances[currentValve, valve]
            if currentValve != start:
                maxPressureReleased = max(maxPressureReleased, search(valve, tuple(list(openValves[:currentValve]) + [1] + list(openValves[currentValve+1:])), timeLeft-distance-1) + goodValves[currentValve] * (timeLeft-1))
            maxPressureReleased = max(maxPressureReleased, search(valve, openValves, timeLeft-distance))
        return maxPressureReleased
    else:
        return 0

print(search(start, tuple(0 for _ in range(len(goodValves))), maxTime))

inputfile.close()