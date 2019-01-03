from visulization import visualization
import pygame
from Node import *
from RRT import *

def SampleFreeN(n):
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
                print("hit self")
            elif distNodeToNode(z,v) < r_z :
                z.near.append(v)
        z.saved = True
        return z.near


def getRz():
    #to be coded
    return 10


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

def FMT(start, end):
    V = SampleFreeN(2000)
    vis.nodes = V
    root = Node(start[0],start[1])
    vis.root = root
    z = root
    V.append(z)
    z.visited = True
    z.open = True
    r_z = getRz()
    N_z = MemoNear(V,z,r_z)
    count  = 0
    print(getOpen(V))

    while(distToPoint(z,end)> acc and count < len(V)):
        count +=1
        #need to write get Closed
        vOpenNew = []
        xNear = getVisited(N_z,visited=False)
        for x in xNear:
            N_x = MemoNear(V,x,r_z)
            yNear = getOpen(N_x)
            print(yNear)
            yMin = min(yNear,key = lambda y:Cost(y)+CostOfEdge(y,x))#arg min line
            if collisionFree(yMin,x,obs):
                yMin.addChild(x)
                vOpenNew.append(x)
                x.visited = True
        setOpen(vOpenNew)
        z.open = False
        z.closed = True
        #relook at closed stuff
        if(len(getOpen(V)) == 0):
            print("failed")
            return 
        z = min(getOpen(V),key = lambda y:Cost(y))
        z.printData()
        N_z = MemoNear(V,z,r_z)
        vis.update()
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
    vis = visualization(size,root,target_ = target,scale_= 4,accuracy_=acc,obstacles_=obs)
    vis.path = FMT((0,0),target)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        vis.update()