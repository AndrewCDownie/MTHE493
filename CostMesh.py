import numpy as np
from scipy.stats import multivariate_normal
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

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

    
if __name__ == "__main__":
    m = CostMesh((100,100))
    m.addDetection((50,50))
    plt.imshow(m.mesh)
    plt.show()
    m.addDetection((55,50))
    m.decay()
    plt.imshow(m.mesh)
    plt.show()
    m.addDetection((60,51))
    m.decay()
    plt.imshow(m.mesh)
    plt.show()
    m.addDetection((70,51))
    m.decay()
    plt.imshow(m.mesh)
    plt.show()
    m.addDetection((80,51))
    m.decay()
    plt.imshow(m.mesh)
    plt.show()
    m.addDetection((50,50))
    plt.imshow(m.mesh)
    plt.show()
    m.addDetection((55,60))
    m.decay()
    plt.imshow(m.mesh)
    plt.show()
    m.addDetection((60,65))
    m.decay()
    plt.imshow(m.mesh)
    plt.show()
    m.addDetection((70,80))
    m.decay()
    plt.imshow(m.mesh)
    plt.show()
    m.addDetection((80,90))
    m.decay()
    plt.imshow(m.mesh)
    plt.show()

