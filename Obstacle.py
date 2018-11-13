import math
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString

class obstacle(object):

    #Initializes the polygon which represents the obstacle
    def __init__(self,points_):
        self.points = Polygon(points_)

    #Checks to see if a given point is within an obstacle including if it is on the boundary
    #Returns true if the point is in the shape
    #Returns false if the point is not in the shape            
    def checkInside(self,point):
        checkpoint=Point(point)
        flag=self.points.intersects(checkpoint)
        return flag

    #Checks to see if a line is within an obstacle, point 1 refers to current position and point 2 is where it wants to go
    #Returns true if the line passes through the shape
    #Returns false if the line does not pass through the shape
    def checkPassThrough(self,point1,point2):
        line = LineString([point1,point2])
        flag=self.points.intersects(line)
        return flag

    #Print the max bounds and min bounds for x and y in that order
    def printPoints(self):
        print(self.points.bounds)