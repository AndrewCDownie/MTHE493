import numpy as np
from scipy.stats import multivariate_normal
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from Obstacle import obstacle
from pathPlanningUtils import *

class CostMesh(object):

    def __init__(self,size_,):
        self.size = size_
        self.mesh = np.zeros(size_)
        self.detection = 0
    
    def checkBound(self,point):
        x = round(point[0])
        y = round(point[1])
        return 0<= x < self.size[0] and 0<= y <self.size[1]

    def getMeshCopy(self):
        newMesh = CostMesh(self.size)
        newMesh.mesh = np.copy(self.mesh)
        return newMesh
        

    def getCost(self,point):
        #add scaling in later
        x = int(round(point[0]))
        y = int(round(point[1]))
        if 0<= x < self.size[0] and 0<= y <self.size[1]:
            return self.mesh[x][y]
        else:
            return 0
    
    def addDetection(self, point):
        gain = 100
        x = int(round(point[0]))
        y = int(round(point[1]))
        gaussian = multivariate_normal([point[0],point[1]],[[10,0],[0,10]])
        for i in range(x-50,x+50):
            for j in range(y-50,y+50):
                if self.checkBound((i,j)):
                    val = gain*gaussian.pdf((i,j))
                    if val > 0.0001:
                        self.mesh[i,j] += val
        return
    
    def decay(self):
        self.mesh = 0.40*self.mesh
        return

    def initSensitivity(self, obstacles):
        for i in range (0, self.size[0]):
            for j in range (0,self.size[1]):
                self.mesh[i,j]=1
        self.setUpSensitivity(obstacles[0].rawpoints[0],obstacles[0].rawpoints[1],obstacles[0].rawpoints[2],obstacles[0].rawpoints[3])
        return
    
    def setUpSensitivity(self,obst, objectul, objectur, objectlr, objectll):
        density=0.5
        line1_x = np.linspace(obst.rawpoints[0][0],obst.rawpoints[1][0],density*distToPoint(obst.rawpoints[0],obst.rawpoints[1],p2p = True))
        line1_y = np.linspace(obst.rawpoints[0][1],obst.rawpoints[1][1],density*distToPoint(obst.rawpoints[0],obst.rawpoints[1],p2p = True))
        for i in range(len(line1_x)):
            hpoint=(line1_x[i],line1_y[i])
            self.addDetection(hpoint)
        
        """
        numpointswidth=int(density*(objectur[0]-objectul[0]))
        numpointsheight=int(density*(objectll[1]-objectul[1]))
        print(numpointswidth)
        print(numpointswidth)
        print(objectur[0])
        print(objectur[1])
        print(objectlr[0])
        print(objectll[1])
        widthpoints=np.linspace(objectur[0],objectul[0],int(numpointswidth))
        heightpoints=np.linspace(objectlr[1],objectur[1],int(numpointsheight))
        for i in range (0,numpointsheight):
            hpoint=(objectur[0],heightpoints[i])
            self.addDetection(hpoint)
        for j in range (0,numpointswidth):
            wpoint=(widthpoints[j],objectul[0])
            self.addDetection(wpoint)
        for i in range (0,numpointsheight):
            hpoint2=(objectul[0],heightpoints[i])
            self.addDetection(hpoint2)
        for j in range (0,numpointswidth):
            wpoint2=(widthpoints[j],objectll[0])
            self.addDetection(wpoint2)
        """
        return

    
if __name__ == "__main__":
    m = CostMesh((200,200))
    obs = [
        obstacle([(20,20),(20,40),(80,40),(80,20)]),
        obstacle([(20,20+30),(20,40+30),(80,40+30),(80,20+30)]),
        obstacle([(90,30),(90,80),(100,80),(100,30)])
    ]
    m.initSensitivity(obs)

    #m.addDetection((50,50))
    plt.imshow(m.mesh)
    plt.show()
   
