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
        self.path = []

    def CheckEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:  # or MOUSEBUTTONDOWN depending on what you want.
                print(event.pos)
                self.clickedPoints.append(self.getScaledPoint(event.pos))
                print(self.clickedPoints)
    
    def setNewRoot(self,newRoot):
        self.root =newRoot
        self.vis.root= newRoot

    def setNewTarget(self,newTarget):
        self.target = newTarget
        self.vis.target = (math.floor(newTarget[0]),math.floor(newTarget[1]))

    def getScaledPoint(self,point):
        return (point[0]/self.scale,point[1]/self.scale)

    def addPath(self,path_):
        for elem in reversed(path_):
            self.path.insert(0,elem)
        self.vis.path = self.path
        pygame.event.get()
        self.vis.update()