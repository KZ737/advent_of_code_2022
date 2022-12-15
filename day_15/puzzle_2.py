import re
inputfile = open("./day_15/input.txt", "r")

'''
Calculates the Manhattan distance between two points.
'''
def distance(sensor, beacon):
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])

'''
We store the coordinates of the sensors and their distance to the closest beacons.
This time we don't need to store the coordinates of the beacons.
But we store another property instead.
The sensors create a square shape region around themselves in which there cannot be any beacons.
This means that inside the search area, if there is only one point where there can be a beacon, it must be _just_ outside of at least 2 beacons' region (i.e. there are at least two sensors from which the point is just 1 unit farther than their corresponding closest beacons).
The square shapes can be described by 4 lines, 2 with slopes = 1, 2 with slopes = -1.
Then, if we store all the lines (i.e. all their y-intercepts), and check all intersections between the positive and the negative slope lines, we get all the points where the sole missing beacon can be.
The justOutsideLines list does exactly that, justOutsideLines[0] stores the y-intercepts of all slope = 1 lines, and justOutsideLines[1] those with a slope of -1.
'''
pattern = "Sensor at x=(?P<sensorX>[-]?[0-9]+), y=(?P<sensorY>[-]?[0-9]+): closest beacon is at x=(?P<beaconX>[-]?[0-9]+), y=(?P<beaconY>[-]?[0-9]+)"
sensors = {}
justOutsideLines = [[], []]
for line in inputfile:
    m = re.search(pattern, line)
    sensorX, sensorY, beaconX, beaconY = map(int, m.groups())
    sensorBeaconDistance = distance((sensorX, sensorY), (beaconX, beaconY))
    sensors.update({(sensorX, sensorY): sensorBeaconDistance})
    justOutsideLines[0].extend([sensorY-sensorX+sensorBeaconDistance+1, -sensorY-sensorX+sensorBeaconDistance+1])
    justOutsideLines[1].extend([sensorY+sensorX+sensorBeaconDistance+1, -sensorY+sensorX+sensorBeaconDistance+1])

'''
We are looking for points in the (0, 0) - (4000000, 4000000) range.
Now we calculate the intersections of the aforementioned lines.
If an intersection's x coordinate is at a non-integer coordinate, we ignore it.
If it is at an integer coordinate, we calculate the intersection's y coordinate from the equation of any of the lines (I used the line with a slope of 1).
Then we check if both the x and y coordinates are inside the bounds, if they are not, we ignore the intersection.
If it is inbounds, we iterate over all sensors and see if the sensor is closer to the intersection than it is to its closest beacon; if it is, then that obviously means that there is no beacon there, because then that would've been the closest beacon. If this happens, we break from the loop and start looking at a new intersection.
But if the intersection is not closer to any sensors than they are to their beacons, that means we found the missing point, so we print the missing point's tuning frequency, then break from the loop.
'''
bounds = [0, 4000000]
for positiveLine in justOutsideLines[0]:
    for negativeLine in justOutsideLines[1]:
        intersectionX = (negativeLine - positiveLine) / 2
        if float.is_integer(intersectionX):
            intersectionX = int(intersectionX)
        else:
            continue
        intersectionY = intersectionX + positiveLine
        if (bounds[0] > intersectionX) or (bounds[1] < intersectionX) or (bounds[0] > intersectionY) or (bounds[1] < intersectionY):
            continue
        insideAnOtherRegion = False
        for sensor, beaconDistance in sensors.items():
            if abs(sensor[0]-intersectionX) + abs(sensor[1]-intersectionY) < beaconDistance:
                insideAnOtherRegion = True
                break
        if insideAnOtherRegion:
            continue
        else:
            print(intersectionX*4000000 + intersectionY)
            break

inputfile.close()