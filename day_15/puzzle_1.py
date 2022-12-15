import re
inputfile = open("./day_15/input.txt", "r")

'''
Calculates the Manhattan distance between two points.
'''
def distance(sensor, beacon):
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])

'''
We store the coordinates of the sensors and their distance to the closest beacons.
We also store the coordinates of the beacons so that we don't accidentally count a beacon in the "cannot contain beacons" set.
'''
pattern = "Sensor at x=(?P<sensorX>[-]?[0-9]+), y=(?P<sensorY>[-]?[0-9]+): closest beacon is at x=(?P<beaconX>[-]?[0-9]+), y=(?P<beaconY>[-]?[0-9]+)"
sensors = {}
beacons = set()
for line in inputfile:
    m = re.search(pattern, line)
    sensorX, sensorY, beaconX, beaconY = map(int, m.groups())
    sensors.update({(sensorX, sensorY): distance((sensorX, sensorY), (beaconX, beaconY))})
    beacons.add((beaconX, beaconY))

'''
We are searching on the 2000000th line.
We start out with an empty set, which will contain the coordinates where there cannot be beacons.
We iterate over all sensors, and if the sensor is closer to y = 2000000 than its distance is to its closest beacon, then it means that there is some range on the y = 2000000 line where there cannot be beacons. This range is centered on the x coordinate of the sensor, and has a radius of (the distance to the closest beacon from the sensor - the distance to y = 2000000 from the sensor). If the points in this range are not beacons themselves, then we add them to the set of coordinates where there cannot be any beacons.
The size of this set will be the number of coordinates where there cannot be beacons.
'''
y = 2000000
cannotContain = set()
for sensor, beaconDistance in sensors.items():
    if abs(sensor[1] - y) <= beaconDistance:
        horizontalCoverage = beaconDistance - abs(sensor[1] - y)
        for i in range(horizontalCoverage+1):
            if (sensor[0]+i, y) not in beacons:
                cannotContain.add(sensor[0]+i)
            if (sensor[0]-i, y) not in beacons:
                cannotContain.add(sensor[0]-i)

print(len(cannotContain))

inputfile.close()