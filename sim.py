from visulization import *
from RRT import *
from Obstacle import *
from FMT import *
from state import state
from pathPlanningUtils import measurePathLength
import numpy as np 
import matplotlib.pyplot as plt


class robot(object):
    def __init__(self,position_,radius_ = 12):
        self.position = position_
        self.radius = radius_
        self.pathToGo = []
        self.preDetections = []


    def checkDetected(self, state):
        toDelete = []
        detected = True
        for preDetect in self.preDetections:
            if distToPoint(self.position,preDetect,p2p=True)< self.radius:
                print("Detected:")
                print(preDetect)
                state.addDetectedPoint(preDetect)
                state.vis.detectedPoints.append(preDetect)
                toDelete.append(preDetect)
                detected = False
        
        for elem in toDelete:
            self.preDetections.remove(elem)
        print(self.preDetections)
        return detected

    def preparePath(self,path):
        interPath = []
        for i in range(1, len(path)):
            p1 = path[i-1].getPoint()
            p2 = path[i].getPoint()
            x_s = np.linspace(p1[0],p2[0],num = 5)
            y_s = np.linspace(p1[1],p2[1],num = 5)
            interSec = zip(x_s,y_s)
            for elem in interSec:
                self.pathToGo.append(elem)
                interPath.append(elem)
        return interPath


    def go(self,state,path_):
        detectedNum = 0
        
        print(self.preDetections)
        path = list(path_)
        state.mode = "other"
        self.pathToGo = []
            #path = list(reversed(path))
        travelledPath = []
        self.preparePath(path)
        state.vis.pathToGo = list(self.pathToGo)
        state.vis.update()
        state.CheckEvents()
        #stop traversing to reroute 
        instantCost = state.costMesh.getMeshCopy()
        while len(self.pathToGo)>0:
            state.mode = "traversing"
            time.sleep(0.1)
            self.position = (int(round(self.pathToGo[0][0])),int(round(self.pathToGo[0][1])))
            travelledPath.append(self.position)
            state.vis.robotPos = self.position
            state.vis.update()
            state.CheckEvents()
            travelledPath.append(self.pathToGo.pop(0))
            if(not self.checkDetected(state)):
                detectedNum +=1
                (reRoutePath,reRouteGoal, success) = reRoute(state,self,instantCost)
                if(success):
                    reRouteGoalindex = self.pathToGo.index(reRouteGoal)
                    endPath = self.pathToGo[reRouteGoalindex:]
                    self.pathToGo = []
                    self.preparePath(reRoutePath)
                    self.pathToGo = self.pathToGo + endPath
                else:
                    self.pathToGo = []
                    self.preparePath(reRoutePath) 
                state.vis.pathToGo = list(self.pathToGo)


                    
        return travelledPath, detectedNum 

        


        


if __name__ == "__main__":
    obs = []
    travelled = []
    planned = []
    encoutered= []
    obs = [
        obstacle([(10, 10), (10, 20), (40, 20), (40, 10)]),
        obstacle([(10, 25), (10, 35), (40, 35), (40, 25)]),
        obstacle([(10, 40), (10, 50), (40, 50), (40, 40)]),
        obstacle([(10, 55), (10, 65), (40, 65), (40, 55)]),
        obstacle([(10, 70), (10, 80), (40, 80), (40, 70)]),

        obstacle([(60, 10), (60, 20), (90, 20), (90, 10)]),
        obstacle([(60, 25), (60, 35), (90, 35), (90, 25)]),
        obstacle([(60, 40), (60, 50), (90, 50), (90, 40)]),
        obstacle([(60, 55), (60, 65), (90, 65), (90, 55)]),
        obstacle([(60, 70), (60, 80), (90, 80), (90, 70)]),

        obstacle([(100, 10), (100, 40), (110,40), (110,10)]),
        obstacle([(120, 10), (120, 40), (130, 40), (130, 10)]),
        obstacle([(140, 10), (140, 40), (150, 40), (150, 10)]),

        obstacle([(100, 40+10), (100, 40+40), (110, 40+40), (110,40+ 10)]),
        obstacle([(120, 40+10), (120,40+ 40), (130,40+ 40), (130,40+ 10)]),
        obstacle([(140, 40+10), (140,40+ 40), (150,40+ 40), (150,40+ 10)]),

    ]

    size = (150,100)
    root = Node(0,0)
    target = (40,5)
    acc = 3
    state = state(size,5,acc,root,target,obs,name_ = "Path Planning Simulation")
    state.setRobot(robot(state.root.getPoint()))

    destinationQueue =[(70.0, 5.0),(76.8, 38),
    (76.2, 52.8), 
    (115.2, 23.0),
    (27.0, 22.0),
    (73.8, 85.2),
    (70.0, 5.0), 
    (76.8, 37.4),
    (74.2, 52.8), 
    (115.2, 23.0),
    (27.0, 22.0),
    (73.8, 85.2)]

    detectionSets = [[(50,0)],
    [(50,20),(50,0)],
    [(50,20),(52,35)],
    [(92,30),(50,20),(42,35)],
    [(92,30),(50,15),(45,70)],
    [(50,65),(52,17),(47,35)],
    [(50,65),(48,20),(50,40)],
    [(10,10),(50,20),(52,54)],
    [(50,20),(50,10)],[(50,20),(52,35)],
    [(92,30),(50,20),(42,35)],
    [(92,30),(50,15),(45,70)],
    [(50,65),(52,17),(47,35)],
    [(50,65),(48,20),(50,40)],
    [(10,10),(50,20),(52,54)]]
    


    state.robot.preDetections = detectionSets.pop(0)
    state.target = destinationQueue.pop(0)
    #vis = visualization(size,root,target_ = target,scale_= 4,accuracy_=acc,obstacles_ = obs)
    path = reRouteTotal(state,(0, 0),state.target,1500)
    state.setCurPath(path)

    state.vis.root = Node(0,0)
    state.vis.nodes = []
    (travelledPath, encouteredNum) = state.robot.go(state,path)
    encoutered.append(encouteredNum)
    state.vis.travelledPath = travelledPath
    state.setCurPath([])
    state.addPath(path)
    state.noReroutePath = state.noReroutePath + path
    plannedPathLength = measureNodePathLength(state.noReroutePath)
    travelledPathLength = measurePathLength(travelledPath)
    print(measureNodePathLength(state.noReroutePath))
    print(measurePathLength(travelledPath))
    travelled.append(travelledPathLength)
    planned.append(plannedPathLength)
    state.costMesh.decay(0.7)
    state.mode = "Schedualed"
    running = True 
    
    while running:
        state.mode = "Schedualed"
        if len(destinationQueue)>0 and len(detectionSets)>0:
            nextDest = destinationQueue.pop(0)
            state.target = nextDest
            state.robot.preDetections = detectionSets.pop(0)
            path = []
            i = 0
            while len(path)==0:
                path = reRouteTotal(state,state.robot.position,nextDest,1500+i)
                i+=100
            state.setCurPath(path)
            state.vis.root = Node(0,0)
            state.vis.nodes = []
            (tPath, encouteredNum) = state.robot.go(state,path)
            encoutered.append(encouteredNum)
            travelledPath = travelledPath + tPath
            state.vis.travelledPath = travelledPath
            state.setCurPath([])
            state.addPath(path)
            state.noReroutePath = state.noReroutePath + path
            plannedPathLength = measureNodePathLength(state.noReroutePath)
            travelledPathLength = measurePathLength(travelledPath)
            print(measureNodePathLength(state.noReroutePath))
            print(measurePathLength(travelledPath))
            
            travelled.append(travelledPathLength)
            planned.append(plannedPathLength)
            print(planned)
            print(travelled)
            print(encoutered)
            state.costMesh.decay(0.7)
            """
            plt.plot(travelled)
            plt.plot(planned)
            plt.show()
            state.costMesh.decay(1)
            """


        
        """
        Get statistics make cost mesh work!
        """
        state.vis.root = Node(0,0)

        state.CheckEvents()
        state.vis.update()