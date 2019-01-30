from Node import *
from Obstacle import *
from visulization import *
import math
class state(object):

    def __init__(self,size_,scale_,acc_,root_,target_,obstacles_,name_ = ""):
        self.root = root_
        self.size = size_
        self.scale = scale_
        self.obstacles = obstacles_
        self.acc = acc_
        self.target = target_
        self.vis = visualization(self.size,self.root,target_ = self.target,scale_= self.scale ,accuracy_=self.acc,obstacles_ = self.obstacles,name=name_)
        self.clickedPoints = []
        self.curPath = []
        self.totalPath = []
        self.detectedPoints = []

    def CheckEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:  # or MOUSEBUTTONDOWN depending on what you want.
                print(event.pos)
                self.clickedPoints.append(self.getScaledPoint(event.pos))
                print(self.clickedPoints)
                self.addDetectedPoint(self.getScaledPoint(event.pos))
            if event.type == pygame.QUIT:
                exit()
    
    def getPointCost(self,point):
        gain = 3
        var= 10
        cost = 0
        #loop through all the points and sum of costs
        for detected in self.detectedPoints:
            dist = distToPoint(point, detected, p2p = True)
            cost +=gain*math.exp((-dist**2)/(2*var))
        return cost
    #added point to detected list 
    def addDetectedPoint(self,p):
        #check inside each obstacle
        for obj in self.obstacles:
            if(obj.checkInside(p)):
                #reject the point 
                return
        self.detectedPoints.append(p)

    def dropDectections(self):
        self.detectedPoints = []

    def setNewRoot(self,newRoot):
        self.root =newRoot
        self.vis.root= newRoot

    def setNewTarget(self,newTarget):
        self.target = newTarget
        self.vis.target = (math.floor(newTarget[0]),math.floor(newTarget[1]))

    def setRobot(self,newRobot):
        self.robot = newRobot
        self.vis.robot = newRobot
        self.vis.robotRadius = newRobot.radius

    def getScaledPoint(self,point):
        return (point[0]/self.scale,point[1]/self.scale)

    def addPath(self,path_):
        self.curPath = []
        for elem in reversed(path_):
            self.totalPath.insert(0,elem)
            self.curPath.insert(0,elem)
        self.vis.path = self.totalPath
        pygame.event.get()
        self.vis.update()