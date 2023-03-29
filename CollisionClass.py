from math import inf, dist
from PlayerClass import player


class Line:
    def __init__(self, x1=None, y1=None, x2=None, y2=None, direction=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.direction = direction
        self.xi1 = None
        self.yi1 = None
        self.xi2 = None
        self.yi2 = None

    # used to set the coordinates of the line objects
    def setCoord(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    # used to find the intersection between two line segments
    def intersection(self, lines, projectile):
        shortestCollision = None
        shortest = inf
        for line in lines:
            # used to calculate the direction vectors of both the lines
            s1X = self.x2 - self.x1
            s1Y = self.y2 - self.y1
            s2X = line.x2 - line.x1
            s2Y = line.y2 - line.y1

            # used to check if the lines are parallel,
            # if they are then there cannot be an intersection so None is returned
            if -s2X * s1Y + s1X * s2Y == 0:
                continue

            # calculates the position of intersection along the line for both the lines,
            # this should be between 0 and 1 because it represents a percentage of the line vector
            s = (-s1Y * (self.x1 - line.x1) + s1X * (self.y1 - line.y1)) / (-s2X * s1Y + s1X * s2Y)
            t = (s2X * (self.y1 - line.y1) - s2Y * (self.x1 - line.x1)) / (-s2X * s1Y + s1X * s2Y)

            # if s and t are not both between 0 and 1,
            # then the intersection can not occur between the two segments,
            # so the program returns None
            if 1 < s or s < 0 or 1 < t or t < 0:
                continue

            # this is used to find the actual coordinates of intersection,
            # by multiplying the percentage along the vector by the vector,
            # and adding the original position,
            # this calculates the exact coordinates of intersection for the two line segments
            xi = self.x1 + (t * s1X)
            yi = self.y1 + (t * s1Y)
            distance = dist((xi, yi), (player.x, player.y))
            if projectile.name == 1:
                line.xi1 = xi
                line.yi1 = yi
            elif projectile.name == 2:
                line.xi2 = xi
                line.yi2 = yi
            if distance < shortest:
                shortest = distance
                shortestCollision = line
        return shortestCollision


L1 = Line()
