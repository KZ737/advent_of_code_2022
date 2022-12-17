import numpy as np

'''
Tetris class, basically a decorator around a numpy array. The playing field is the actual numpy array, which contains 2s for stopped objects ("walls"), 0s for air, and temporarily 1s for still moving objects.
The height attribute is the height of the actual playing field, i.e. one less than the height of the numpy array, because the last row of the array is full of 2s, denoting the floor.
'''
class Tetris:
    def __init__(self):
        self.height = 0
        self.playField = np.full((self.height+1, 7), fill_value=2, dtype=np.byte)

    def resize(self, increaseBy):
        self.height += increaseBy
        self.playField = np.pad(self.playField, ((increaseBy, 0), (0, 0)))

'''
Generic shape class. All shapes have heights, position of their origin coordinates (min(x), min(y)), and coordinates relative to the origin where the shape is "solid".
When creating a shape, we resize the playfield it is contained in, such that there is 3 empty rows between the bottommost of the new shape and the top of the rocks in the tetris, i.e. we add (3 + height of the shape) rows to the top of the playing field.
Since the originPosition given to the shape is the leftmost-bottommost corner, its y coordinate must be shifted "up" (lower row in numpy array) by the shape's height-1.
Example:

           next shape is a plus    |.......|                          |.......|                          |...#...|
           its height is 3, so     |.......|  leftmost == 3rd*        |.......|  showing all solid       |..###..|
           we extend the playing   |.......|  bottommost == 3rd**     |..O....|  elements of the         |..O#...|
           field by 3+3 = 6        |.......|                          |.......|  shape                   |.......|
          =======================> |.......| =======================> |.......| =======================> |.......|
                                   |.......|                          |.......|                          |.......|
|..####.|                          |..####.|                          |..####.|                          |..####.|
+-------+                          +-------+                          +-------+                          +-------+

What I call "elements" of the shape, are in this case the coordinates [0, 1], [1, 0], [1, 1], [1, 2], and [2, 1]. The absolute coordinates of individual elements can be calculated by adding the relative coordinates to the absolute coordinates of the origin: [elemAbsX, elemAbsY] = [originX + elemRelX, originY + elemRelY]
* 3rd from the left
** we extended the playing field by 3+height (in this case 3+3=6), and thus we have to shift our bottommost y value (which is the y value of the origin point, denoted by "O") by height-1 as well. (The -1 appears because of 0-based indexing.)
'''
class Shape:
    def __init__(self, originPosition, elements, height, tetris):
        self.height = height
        tetris.resize(3 + self.height)
        self.originPosition = [originPosition[0], originPosition[1] + self.height-1]
        self.elements = elements
        
    '''
    This function moves the shape horizontally on the playing field, if it can be moved to the given direction. Left is -1, right is +1.
    We calculate the absolute x and y coordinates for each element, and add -1 or +1 to the x coordinates.
    If we are at a wall, i.e. any element's x coordinate is not in the interval (0, 6), inclusive, then we break from the loop and do nothing.
    If an element would not collide with a wall but instead finds something different from air in its supposed-to-be new coordinates (notice the inverted x and y coordinates due to the difference between usual spatial coordinates and numpy array axes order), we also break from the loop and do nothing.
    If we didn't break from the loop, i.e. there is nothing to stop our horizontal movement, then we shift the origin's absolute coordinates to the given direction.
    '''
    def moveHorizontally(self, direction, tetris):
        for element in self.elements:
            elemX = self.originPosition[0] + element[0] - 1 if direction == -1 else self.originPosition[0] + element[0] + 1
            elemY = self.originPosition[1] - element[1]
            if elemX < 0 or elemX > 6:
                break
            if tetris.playField[elemY, elemX] != 0:
                break
        else:
            self.originPosition = [self.originPosition[0] + direction, self.originPosition[1]]
    
    '''
    This function moves the shape down on the playing field, if it can be moved, or stops it, if it cannot.
    Very similar to the second comparison of the horizontal movement function, in this case we return True if the shape has come to a stop (meaning that we can start dropping another shape).
    If we can move the shape down, that means that the topmost row might be empty.
    If it actually is empty, we delete that row and decrease the height attribute of the tetris, and since the origin's coordinate is relative to the top of the playing field, this deletion automatically moves the shape down by 1.
    If the topmost row is not empty, we add 1 to the origin's y coordinate.
    In any case, we return False, for the shape has not come to a stop.
    '''
    def moveDown(self, tetris):
        for element in self.elements:
            elemX = self.originPosition[0] + element[0]
            elemY = self.originPosition[1] - element[1] + 1
            if tetris.playField[elemY, elemX] != 0:
                return True
        if not np.any(tetris.playField[0,:]):
            tetris.playField = np.delete(tetris.playField, 0, 0)
            tetris.height -= 1
        else:
            self.originPosition = [self.originPosition[0], self.originPosition[1]+1]
        return False
    
    '''
    This function makes a shape stop, meaning that from now on, its position is fixed.
    We iterate through all elements of the shape and change the playing field's values at all the coordinates to 2.
    '''
    def stop(self, tetris):
        for element in self.elements:
            elemX = self.originPosition[0] + element[0]
            elemY = self.originPosition[1] - element[1]
            tetris.playField[elemY, elemX] = 2
    
    '''
    This was a function for debug purposes, not used in the solution. It prints the current state of the playing field, with empty spaces denoting air, filled boxes denoting solid rocks, and shaded boxes denoting still moving objects.
    It replaces the playing field's values at all the coordinates to 1, prints the array, then replaces them back to 0.
    '''
    def show(self, tetris):
        def drawing(byte):
            if byte == 2:
                return "██"
            elif byte == 1:
                return "▒▒"
            else:
                return "  "
        for element in self.elements:
            elemX = self.originPosition[0] + element[0]
            elemY = self.originPosition[1] - element[1]
            tetris.playField[elemY, elemX] = 1
        print(np.array2string(tetris.playField, max_line_width=np.inf, separator='', formatter={"int": drawing}))
        for element in self.elements:
            elemX = self.originPosition[0] + element[0]
            elemY = self.originPosition[1] - element[1]
            tetris.playField[elemY, elemX] = 0

'''
Class definitions of the possible shapes. All shapes are given initial elements, heights, and names used for debug purposes.
'''

'''
O###
'''
class HorizontalLine(Shape):
    def __init__(self, origin, tetris):
        self.elements = [[0, 0], [1, 0], [2, 0], [3, 0]]
        self.height = 1
        self.name = "Horizontal line"
        super().__init__(origin, self.elements, self.height, tetris)

'''
 # 
###
O# 
'''
class Plus(Shape):
    def __init__(self, origin, tetris):
        self.elements = [[0, 1], [1, 0], [1, 1], [1, 2], [2, 1]]
        self.height = 3
        self.name = "Plus sign"
        super().__init__(origin, self.elements, self.height, tetris)

'''
#
#
#
O
'''
class VerticalLine(Shape):
    def __init__(self, origin, tetris):
        self.elements = [[0, 0], [0, 1], [0, 2], [0, 3]]
        self.height = 4
        self.name = "Vertical line"
        super().__init__(origin, self.elements, self.height, tetris)

'''
##
O#
'''
class Square(Shape):
    def __init__(self, origin, tetris):
        self.elements = [[0, 0], [1, 0], [0, 1], [1, 1]]
        self.height = 2
        self.name = "Square"
        super().__init__(origin, self.elements, self.height, tetris)

'''
  #
  #
O##
'''
class InvertedL(Shape):
    def __init__(self, origin, tetris):
        self.elements = [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]]
        self.height = 3
        self.name = "Inverted L"
        super().__init__(origin, self.elements, self.height, tetris)

'''
We create our field.
The shapes are dropping in the order given in the shapes list.
'''
tetris = Tetris()
shapes = [HorizontalLine, Plus, InvertedL, VerticalLine, Square]

'''
Create a list of -1s and 1s from the input <s and >s, respectively.
'''
inputfile = open("./day_17/input.txt", "r")
directions = [-1 if direction == "<" else 1 for direction in list(inputfile.readline().strip()) ]

'''
The first shape is a horizontal line, which sits at index 0 of the shapes list.
It is placed at the 3rd column from the left, and to the 0th row from below (counting starting at the height+3rd row).
We want to calculate the height after 2022 shapes.
'''
shapeCounter = 0
newShape = shapes[shapeCounter]([2, 0], tetris)
desiredShapeCount = 2022

'''
!!!!!!! IMPORTANT NOTE !!!!!!!
      THIS SOLUTION DOES
      NOT WORK WELL WITH
            PART 2
!!!!!!! IMPORTANT NOTE !!!!!!!

The calculation would take a LOT of time and memory (literally YEARS, and several TERABYTES of RAM). This is only a very naive solution, which is good enough for part 1, but is useless at solving part 2.

We count which loop we are in. Starting from zero, in every even loop we move horizontally, and in every odd loop we move down.
The horizontal movement's direction is set by the directions list, created from the input. Since we move horizontally every 2 loops, we divide the loop counter with 2. We also take modulo length of directions list, so that it repeats in cycles.
If in a loop, we weren't able to move down (the moveDown function returns True), we stop the shape in place, increase the shape counter. If the shape counter gets to the desired value (2022), we break from the loop. If it hasn't reached the desired value yet, then we create a new shape, and place it on the playing field. Since the 5 shapes repeat in cycles, we take the counter's remainder with division with 5.
The 4 commented lines were for debug purposes, and use the aforementioned Shape.show() function and the different shapes' name attribute.
'''
i = 0
while True:
    # newShape.show(tetris)
    if i%2 == 0:
        # print(newShape.name, "moving horizontally", directions[ (i//2) % len(directions) ] )
        newShape.moveHorizontally( directions[ (i//2) % len(directions) ] , tetris)
    else:
        # print(newShape.name, "moving down")
        stopped = newShape.moveDown(tetris)
        if stopped:
            # print(newShape.name, "stopped")
            newShape.stop(tetris)
            shapeCounter += 1
            if shapeCounter == desiredShapeCount:
                break
            newShape = shapes[ shapeCounter % 5 ]([2, 0], tetris)
    i += 1

'''
After finally breaking from the loop, we print the height of the playing field, i.e. the height of the rocks on each other.
'''
print(tetris.height)

inputfile.close()