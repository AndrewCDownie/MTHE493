from visulization import visualization
import pygame
from Node import *
from RRT import *
import time
from state import state
def SampleFreeN(n,obs,size):
    samples = []
    for i in range(n):
        p = SampleFree(obs,size)
        samples.append(Node(p[0],p[1]))
    return samples

def MemoNear(V,z,r_z):
    if z.saved == True:
        return z.near
    else:
        for v in V:
            if(z is v):
                pass
            elif distNodeToNode(z,v) < r_z :
                z.near.append(v)
        z.saved = True
        return z.near


def getRz():
    #to be coded
    return 12


#returns set of that is  weather it is open or closed
def getOpen(V):
    openV = []
    for v in V:
        if v.open == True:
            openV.append(v)
    return openV

#returns visited or unvisited node based on visited var
def getVisited(V,visited = False):
    visitedV = []
    for v in V:
        if v.visited == visited:
            visitedV.append(v)
    return visitedV

def setOpen(V):
    for v in V:
        v.open = True
    return


"""
To make this program run faster

binary min heap needs to be implemented to hold v open

cost at each node should be saved but maybe not because changing nature of the enviroment


QUote from paper "This is because the proof of AO in Theorem 4.1 relies on the cost being additive and obeying the triangle inequality."

REad Section 5.2.1 Metric Costsz


also needs to add robustness to make sure it completes by adding more sampling

"""

def FMT(state,n):
    V = SampleFreeN(n,state.obstacles,state.size)
    state.vis.nodes = V
    z = state.root
    V.append(z)
    z.visited = True
    z.open = True
    r_z = getRz()
    N_z = MemoNear(V,z,r_z)
    count  = 0
    while(distToPoint(z,state.target)> state.acc):
        count +=1
        #need to write get Closed
        vOpenNew = []
        xNear = getVisited(N_z,visited=False)
        for x in xNear:
            N_x = MemoNear(V,x,r_z)
            yNear = getOpen(N_x)
            yMin = min(yNear,key = lambda y:Cost(y)+CostOfEdge(y,x)) #arg min line
            if collisionFree(yMin,x,state.obstacles):
                yMin.addChild(x)
                vOpenNew.append(x)
                x.visited = True
                state.vis.update()
                #pygame.event.get()
                state.CheckEvents()
        setOpen(vOpenNew)
        z.open = False
        z.closed = True
        #relook at closed stuff
        if(len(getOpen(V)) == 0):
            print("failed")
            return 
        z = min(getOpen(V),key = lambda y:Cost(y))
        N_z = MemoNear(V,z,r_z)
        #vis.update()
    return getPathToGoal(z)
    print("Done")


    


if __name__ == "__main__":
    obs = []
    obs = [
        obstacle([(20,20),(20,40),(80,40),(80,20)]),
        obstacle([(20,20+30),(20,40+30),(80,40+30),(80,20+30)]),
        obstacle([(90,30),(90,80),(100,80),(100,30)])
    ]

    size = (150,150)
    root = Node(0,0)
    target = (110,50)
    acc = 5
    state = state(size,5,acc,root,target,obs)
    
    #vis = visualization(size,root,target_ = target,scale_= 4,accuracy_=acc,obstacles_ = obs)
    state.vis.path = FMT(state,1000)
    running = True 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:  # or MOUSEBUTTONDOWN depending on what you want.
                print(event.pos)
        state.vis.update()