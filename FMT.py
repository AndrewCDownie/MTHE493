from visulization import visualization
import pygame
import numpy as np
from Node import *
from RRT import *
import time
from state import state
from pathPlanningUtils import *
from BinHeap import BinHeap


"""
To make this program run faster

binary min heap needs to be implemented to hold v open

cost at each node should be saved but maybe not because changing nature of the enviroment

Quote from paper "This is because the proof of AO in Theorem 4.1 relies on the cost being additive and obeying the triangle inequality."

REad Section 5.2.1 Metric Costsz

also needs to add robustness to make sure it completes by adding more sampling


WE NEED TO USE LINE INTERGRALS FOR COMPUTATION OF COST BETWEEN POINTS 


"""

def reRouteTotal(state, start, end, n):
    state.mode = "TotalReroute"
    V = SampleFreeN(n,state.obstacles,state.size)
    state.vis.target = (int(end[0]),int(end[1]))
    print("Total ReRoute")
    #V = sampleRadius(40,(0,0),state)
    VOpen = BinHeap()
    state.vis.nodes = V
    z = Node(start[0],start[1])
    state.root = z
    state.vis.root = state.root
    V.append(z)
    z.visited = True
    VOpen.insert(z)
    r_z = getRz()
    N_z = MemoNear(V,z,r_z,state)
    count  = 0
    while(distToPoint(z,end) > state.acc):
        count +=1
        #need to write get Closed
        vOpenNew = []
        xNear = getVisited(N_z,visited=False)
        for x in xNear:

            N_x = MemoNear(V,x,r_z,state)
            yNear = getOpen(VOpen,N_x)
            #yMin = min(yNear,key = lambda y:Cost(y)+CostOfEdge(y,x)) #arg min line

            #add check for empty to break
            if(len(yNear) == 0):
                break
                
            yMin = min(yNear,key = lambda y:y.cost+CostLI(y,x,state)) #arg min line#need to change this

            if collisionFree(yMin,x,state.obstacles):
                yMin.addChild(x)
                x.setCost(CostLI(yMin,x,state));
                # update cost here 
                vOpenNew.append(x)
                x.visited = True
                state.vis.update()
                #pygame.event.get()
                state.CheckEvents()
        setOpen(VOpen,vOpenNew)
        z.open = False
        z.closed = True
        #relook at closed stuff
        if(VOpen.currentSize == 0):
            print("failed Total")
            return 
        z = VOpen.delMin()
        N_z = MemoNear(V,z,r_z,state)
        #vis.update()
    #state.mode = "hold"
    return getPathToGoal(z)




def reRoute(state,robot,instantMesh):
    #find the closest node with cheepest cost
    state.mode = "reRouting"
    goalPoint = robot.pathToGo[-1]
    successful = True
    #finding the best node to traverse to
    for point in robot.pathToGo:
        print(instantMesh.getCost(point))
        print(state.getPointCost(point))
        if(instantMesh.getCost(point)==state.getPointCost(point)):
            goalPoint = point
            break
    print(robot.position)
    print(robot.pathToGo[-1])
    print(goalPoint)

    V = sampleRadius(distToPoint(point,robot.position,p2p = True),robot.position,state)
    VOpen = BinHeap()
    state.vis.nodes = V
    z = Node(robot.position[0],robot.position[1])
    state.root = z
    V.append(z)
    z.visited = True
    VOpen.insert(z)
    r_z = 20
    N_z = MemoNear(V,z,r_z,state)
    count  = 0
    while(distToPoint(z,goalPoint) > 4):
        count +=1
        #need to write get Closed
        vOpenNew = []
        xNear = getVisited(N_z,visited=False)
        for x in xNear:
            N_x = MemoNear(V,x,r_z,state)
            yNear = getOpen(VOpen,N_x)
            #yMin = min(yNear,key = lambda y:Cost(y)+CostOfEdge(y,x)) #arg min line

            #add check for empty to break
            if(len(yNear) == 0):
                break
                
            yMin = min(yNear,key = lambda y:y.cost+CostLI(y,x,state)) #arg min line#need to change this

            if collisionFree(yMin,x,state.obstacles):
                yMin.addChild(x)
                x.setCost(CostLI(yMin,x,state));
                # update cost here 
                vOpenNew.append(x)
                x.visited = True
                state.vis.update()
                #pygame.event.get()
                state.CheckEvents()
        setOpen(VOpen,vOpenNew)
        z.open = False
        z.closed = True
        #relook at closed stuff
        if(VOpen.currentSize == 0):
            print("failed")
            totalReroute = reRouteTotal(state,(robot.position[0],robot.position[1]),state.target,1500)
            return(totalReroute,state.target,False)
        z = VOpen.delMin()
        N_z = MemoNear(V,z,r_z,state)
        #vis.update()
    state.mode = "hold"
    return (getPathToGoal(z),goalPoint,True)




def FMT_(state,n):
    state.mode = "pathPlanning"
    V = SampleFreeN(n,state.obstacles,state.size)
    #V = sampleRadius(40,(0,0),state)
    VOpen = BinHeap()
    state.vis.nodes = V
    z = state.root
    V.append(z)
    z.visited = True
    VOpen.insert(z)
    r_z = getRz()
    N_z = MemoNear(V,z,r_z,state)
    count  = 0
    while(distToPoint(z,state.target) > state.acc):
        count +=1
        #need to write get Closed
        vOpenNew = []
        xNear = getVisited(N_z,visited=False)
        for x in xNear:
            N_x = MemoNear(V,x,r_z,state)
            yNear = getOpen(VOpen,N_x)
            #yMin = min(yNear,key = lambda y:Cost(y)+CostOfEdge(y,x)) #arg min line

            #add check for empty to break
            if(len(yNear) == 0):
                break
                
            yMin = min(yNear,key = lambda y:y.cost+CostLI(y,x,state)) #arg min line#need to change this

            if collisionFree(yMin,x,state.obstacles):
                yMin.addChild(x)
                x.setCost(CostLI(yMin,x,state));
                # update cost here 
                vOpenNew.append(x)
                x.visited = True
                state.vis.update()
                #pygame.event.get()
                state.CheckEvents()
        setOpen(VOpen,vOpenNew)
        z.open = False
        z.closed = True
        #relook at closed stuff
        if(VOpen.currentSize == 0):
            print("failed")
            return 
        z = VOpen.delMin()
        N_z = MemoNear(V,z,r_z,state)
        #vis.update()
    state.mode = "hold"
    return getPathToGoal(z)


    


if __name__ == "__main__":
    obs = []
    obs = [
        obstacle([(20,20),(20,40),(80,40),(80,20)]),
        obstacle([(20,20+30),(20,40+30),(80,40+30),(80,20+30)]),
        obstacle([(90,30),(90,80),(100,80),(100,30)])
    ]

    size = (150,75)
    root = Node(0,0)
    target = (110,50)
    acc = 5
    state = state(size,5,acc,root,target,obs)
    
    #vis = visualization(size,root,target_ = target,scale_= 4,accuracy_=acc,obstacles_ = obs)
    #state.vis.path = FMT(state,1000)
    print(CostLI(Node(0,0),Node(10,10),state))

    running = True 
    while running:
        state.CheckEvents()
        state.vis.update()
        print(CostLI(Node(0,0),Node(10,10),state))
