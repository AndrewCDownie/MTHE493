from visulization import *
from RRT import *
from Obstacle import *
from FMT import *
from state import state
import numpy as np 


class robot(object):
    def __init__(self,position_,radius_ = 15):
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
        print("got here")
        instantCost = state.costMesh.getMeshCopy()
        while len(self.pathToGo)>0:
            state.mode = "traversing"
            time.sleep(0.1)
            self.position = (int(self.pathToGo[0][0]),int(self.pathToGo[0][1]))
            travelledPath.append(self.position)
            state.vis.robotPos = self.position
            state.vis.update()
            state.CheckEvents()
            travelledPath.append(self.pathToGo.pop(0))
            if(not self.checkDetected(state)):
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


                    
        return travelledPath

        


        


if __name__ == "__main__":
    obs = []
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

        obstacle([(100, 10), (100, 40), (110, 40), (110, 10)]),
        obstacle([(120, 10), (120, 40), (130, 40), (130, 10)]),
        obstacle([(140, 10), (140, 40), (150, 40), (150, 10)]),

    ]

    size = (150,100)
    root = Node(0,0)
    target = (40,5)
    acc = 5
    state = state(size,5,acc,root,target,obs,name_ = "SUPER SIM")
    state.setRobot(robot(state.root.getPoint()))

    destinationQueue =[(27.0, 22.0), (73.8, 37.4), (74.2, 51.8), (77.2, 37.4)]
    detectionSets = [[(50,20),(57,40)],[(50,20),(54,40)],[(50,20),(57,40)],[(50,20),(57,40)]]
    state.robot.preDetections = detectionSets.pop(0)
    #vis = visualization(size,root,target_ = target,scale_= 4,accuracy_=acc,obstacles_ = obs)
    path = reRouteTotal(state,(0,0),(15,5),1800)
    state.setCurPath(path)

    
    print(path)
    travelledPath = state.robot.go(state,path)
    state.vis.travelledPath = travelledPath
    state.setCurPath([])
    state.addPath(path)
    state.noReroutePath = state.noReroutePath + path
    state.mode = "Schedualed"

    running = True 
    
    while running:
        state.mode = "Schedualed"
        if len(destinationQueue)>0:
            nextDest = destinationQueue.pop(0)
            state.robot.preDetections = detectionSets.pop(0)
            path = reRouteTotal(state,state.robot.position,nextDest,1800)
            state.setCurPath(path)
            tPath = state.robot.go(state,path)
            travelledPath = travelledPath + tPath
            state.vis.travelledPath = travelledPath
            state.setCurPath([])
            state.addPath(path)
            state.noReroutePath = state.noReroutePath + path
       

        
        """
            FOR TESTING EVALUATION
            CREATE A SEQUENCE OF POINTS TO TRAVEL TOO
            MEASURE THE OVERALL DISTANCE PATH PLANNED
            ADD ROBOT TO DETECT POINTS FROM LIST
            Refector go to deal with rerouting and calling rerouting functions
        """




        """
            Call FMT to initalize route
            drive toward goal location
            - check if reroute
            - check update current path with reroute
            - drive towards goal with new path
            - check for cost changes 
            - 

        """


        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:  # or MOUSEBUTTONDOWN depending on what you want.
                newRoot= Node(state.vis.path[-1].x, state.vis.path[-1].y)
                newTarget = state.getScaledPoint(event.pos)
                state.setNewRoot(newRoot)
                state.setNewTarget(newTarget) d
                state.vis.nodes = []
                state.dropDectections()
                newPath = FMT(state,1000)
                state.setCurPath(newPath)
                state.robot.go(state)
                state.addPath(newPath)
        """
        state.CheckEvents()
        state.vis.update()