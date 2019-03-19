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

    def addSensitivityDetection(self, point):
        thresh = 2
        gain = 1.5
        x = int(round(point[0]))
        y = int(round(point[1]))
        gaussian = multivariate_normal([point[0],point[1]],[[10,0],[0,10]])
        for i in range(x-50,x+50):
            for j in range(y-50,y+50):
                if self.checkBound((i,j)):
                    val = gain*gaussian.pdf((i,j))
                    if val > 0.0001:
                        if(self.mesh[i,j] + val < thresh):
                            self.mesh[i,j] += val
                        else:
                            self.mesh[i,j] = thresh

    def addDetection(self, point):
        thresh = 5
        gain = 200
        x = round(point[0])
        y = round(point[1])
        gaussian = multivariate_normal([point[0],point[1]],[[15,0],[0,15]])
        scalefactor = thresh/gaussian.pdf((point[0],point[1]))
        for i in range(x-100,x+100):
            for j in range(y-100,y+100):
                if self.checkBound((i,j)):
                    val = scalefactor*gaussian.pdf((i,j))
                    if val > 0.0001:
                        self.mesh[i,j] += val
        plt.imshow(np.transpose(self.mesh))
        plt.show()
        return
    
    def decay(self):
        self.mesh = 0.40*self.mesh
        return

    def initSensitivity(self, obstacles):
        for i in range (0, self.size[0]):
            for j in range (0,self.size[1]):
                self.mesh[i,j]=1
        for k in range (0,len(obstacles)):
            self.setUpSensitivity(obstacles[k])
        return
    
    def setUpSensitivity(self,obst):
        density=0.5
        line1_x = np.linspace(obst.rawpoints[0][0],obst.rawpoints[1][0],int(density*distToPoint(obst.rawpoints[0],obst.rawpoints[1],p2p = True)))
        line1_y = np.linspace(obst.rawpoints[0][1],obst.rawpoints[1][1],int(density*distToPoint(obst.rawpoints[0],obst.rawpoints[1],p2p = True)))
        for i in range(len(line1_x)-1):
            hpoint=(line1_x[i],line1_y[i])
            self.addSensitivityDetection(hpoint)

        line1_x = np.linspace(obst.rawpoints[1][0],obst.rawpoints[2][0],int(density*distToPoint(obst.rawpoints[1],obst.rawpoints[2],p2p = True)))
        line1_y = np.linspace(obst.rawpoints[1][1],obst.rawpoints[2][1],int(density*distToPoint(obst.rawpoints[1],obst.rawpoints[2],p2p = True)))
        for i in range(len(line1_x)-1):
            hpoint=(line1_x[i],line1_y[i])
            self.addSensitivityDetection(hpoint)

        line1_x = np.linspace(obst.rawpoints[2][0],obst.rawpoints[3][0],int(density*distToPoint(obst.rawpoints[2],obst.rawpoints[3],p2p = True)))
        line1_y = np.linspace(obst.rawpoints[2][1],obst.rawpoints[3][1],int(density*distToPoint(obst.rawpoints[2],obst.rawpoints[3],p2p = True)))
        for i in range(len(line1_x)-1):
            hpoint=(line1_x[i],line1_y[i])
            self.addSensitivityDetection(hpoint)

        line1_x = np.linspace(obst.rawpoints[3][0],obst.rawpoints[0][0],int(density*distToPoint(obst.rawpoints[3],obst.rawpoints[0],p2p = True)))
        line1_y = np.linspace(obst.rawpoints[3][1],obst.rawpoints[0][1],int(density*distToPoint(obst.rawpoints[3],obst.rawpoints[0],p2p = True)))
        for i in range(len(line1_x)-1):
            hpoint=(line1_x[i],line1_y[i])
            self.addSensitivtyDetection(hpoint)
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
   
