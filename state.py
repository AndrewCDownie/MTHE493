from Node import *
from Obstacle import *
from visulization import *
import FMT
import math
import numpy as np
from CostMesh import CostMesh
class state(object):

    def __init__(self,size_,scale_,acc_,root_,target_,obstacles_,name_ = ""):
        self.mode = "hold"
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
        self.costMesh = CostMesh(self.size)
        self.noReroutePath = []
        self.robot = None
        
    def CheckEvents(self):
        #print("mode:"+ self.mode)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if self.mode == "pathPlanning":
                if event.type == pygame.MOUSEBUTTONUP:  # or MOUSEBUTTONDOWN depending on what you want.
                    print(event.pos)
                    self.clickedPoints.append(self.getScaledPoint(event.pos))
                    print(self.clickedPoints)
                    self.addDetectedPoint(self.getScaledPoint(event.pos))
                    #if(distToPoint(event.pos,self.robot.robotPos,p2p=True)):


            if self.mode == "traversing":
                if event.type == pygame.MOUSEBUTTONUP: 
                    print(distToPoint(self.getScaledPoint(event.pos),self.robot.position,p2p=True)) # or MOUSEBUTTONDOWN depending on what you want.
                    if(distToPoint(self.getScaledPoint(event.pos),self.robot.position,p2p=True)< self.robot.radius):
                        
                        #Setup and ReRoute
                        instantCost = self.costMesh.getMeshCopy()
                        self.addDetectedPoint(self.getScaledPoint(event.pos))
                        (reRoutePath,reRouteGoal, success) = FMT.reRoute(self,self.robot,instantCost)

                        #process rerouted Path
                        reRouteStart = min(self.curPath, key = lambda x:distToPoint(x,self.robot.position))
                        traversedPath = list(self.curPath[:self.curPath.index(reRouteStart)])
                        

                        #Change output based on reroute succes
                        if(success):
                            reRouteGoal = min(self.curPath, key = lambda x:distToPoint(x,reRouteGoal))
                            self.curPath = self.curPath[self.curPath.index(reRouteGoal):]
                            self.curPath = reRoutePath + self.curPath
                        else:
                            self.curPath = reRoutePath
                        self.addPath(traversedPath)
                        self.setCurPath(self.curPath)
                        self.robot.go(self)
                        return False
            
            if self.mode == "Schedualed":
                if event.type == pygame.MOUSEBUTTONUP:  # or MOUSEBUTTONDOWN depending on what you want.
                    print(event.pos)
                    self.clickedPoints.append(self.getScaledPoint(event.pos))
                    print(self.clickedPoints)


            if self.mode == "reRouting":
                pass

            if self.mode == "hold":
                if event.type == pygame.MOUSEBUTTONUP:  # or MOUSEBUTTONDOWN depending on what you want.
                    newRoot= Node(self.robot.position[0], self.robot.position[1])
                    newTarget = self.getScaledPoint(event.pos)
                    self.setNewRoot(newRoot)
                    self.setNewTarget(newTarget)
                    self.vis.nodes = []
                    self.dropDectections()                   
                    newPath = FMT.FMT_(self,2000)
                    self.noReroutePath = self.noReroutePath + newPath
                    self.setCurPath(newPath)
                    self.robot.go(self)
                    self.addPath(self.curPath)
                    self.setCurPath([])
        return True
            
    
    def getPointCost(self,point):
        """
        gain = 3
        var= 10
        cost = 0
        #loop through all the points and sum of costs
        for detected in self.detectedPoints:
            dist = distToPoint(point, detected, p2p = True)
            cost += gain*math.exp((-dist**2)/(2*var))
        return cost
        """


        return self.costMesh.getCost(point)

    #added point to detected list 
    def addDetectedPoint(self,p):
        #check inside each obstacle
        for obj in self.obstacles:
            if(obj.checkInside(p)):
                #reject the point 
                return
        self.detectedPoints.append(p)
        self.costMesh.addDetection(p)

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
        self.totalPath = self.totalPath + path_
        self.vis.path = self.totalPath 
        pygame.event.get()
        self.vis.update()

    def setCurPath(self,path_):
        print(path_)
        self.curPath = path_
        self.vis.curPath= self.curPath
        self.vis.noReroutePath = self.noReroutePath
        pygame.event.get()
        self.vis.update()



