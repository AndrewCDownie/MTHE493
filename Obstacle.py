import math
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString

class obstacle(object):

    def __init__(self,points_):
        self.points = Polygon(points_)

    #Checks to see if a given point is within an obstacle including if it is on the boundary
    #Returns true if the point is in the shape
    #Returns false if the point is not in the shape            
    def checkInside(self,point):
        checkpoint=Point(point)
        flag=self.points.intersects(checkpoint)
        return flag

    #Checks to see if a line is within an obstacle
    #Returns true if the line passes through the shape
    #Returns false if the line does not pass through the shape
    def checkPassThrough(self,point1,point2):
        line = LineString([point1,point2])
        flag=self.points.intersects(line)
        return flag

    def printPoints(self):
        print(self.points.bounds)
