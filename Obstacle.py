class obstacle(object):

    def __init__(self,points_):
        self.points = list(points_)
    
    def checkInside(self,point):
        return False

    def checkPassThrough(self,point1,point2):
        return False

    def printPoints(self):
        for elem in self.points:
            print("("+str(elem[0])+", "+str(elem[1])+")")




obj1 = obstacle([(1,2),(2,2),(3,0)])

obj1.printPoints()

