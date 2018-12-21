import pygame
import random
import time
from Node import *
from Obstacle import *
from RRT import *
from visulization import visualization
import time



if __name__ == "__main__":
    
    running  = True

    #simulations setup
    scale = 7
    obstalce_list = [
        obstacle([(20,20),(20,40),(80,40),(80,20)]),
        obstacle([(20,20+30),(20,40+30),(80,40+30),(80,20+30)]),
        obstacle([(90,30),(90,80),(100,80),(100,30)])
    ]
    cardV = 1
    eta = 2
    acc = 10
    n = 5000
    root = Node(0,0)
    target = (115,95)
    size = (125,100)
    eta = 3
    printed = False
    #create the visualization 
    vis = visualization(size,root,target_ = target, accuracy_ = acc, obstacles_ = obstalce_list, scale_ = 4)
    
    xNewNode = root
    
    gammaRRT = getGammaRRT(3,obstalce_list,size)
    pathsEnds =[]
    path = []
    minPathNode = Node(1,1)
    iterations = 0
    start_time = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #main loop
        iterations +=1
        if(iterations <n):
            xRand = SampleFree(obstalce_list,size)
            xNearest = Nearest(root,xRand)
            xNew = steer(xNearest,xRand,eta)
            if obstacleFree(xNearest,xNew,obstalce_list):
                cMin = 0
                xNewNode = Node(xNew[0],xNew[1])
                ##need to add Card(V)
                #NearPoints = Near(root,xNew,min(eta,gammaRRT*((cardV/(2**cardV))**(1/2))))
                NearPoints = Near(root,xNew,eta)
                xMin = xNearest 
                cMin = Cost(xNearest)+ CostOfEdge(xNearest,xNewNode)
                for xNear in NearPoints:
                    if(collisionFree(xNear,xNew,obstalce_list)and Cost(xNear) + CostOfEdge(xNear,xNewNode)<cMin):
                        xMin = xNear
                        cMin = Cost(xNear) + CostOfEdge(xNear,xNewNode)
                xMin.addChild(xNewNode)
                cardV +=1
                for xNear in NearPoints:
                    if collisionFree(xNear,(xNewNode.x,xNewNode.y),obstalce_list) and Cost(xNewNode)+ CostOfEdge(xNear,xNewNode)< Cost(xNear):

                        xParent = xNear.parent
                        xNewNode.addChild(xNear)
                        xParent.connected.pop(xParent.connected.index(xNear))
                if distToPoint(xNewNode,target)< acc:
                    pathsEnds.append(xNewNode)
            if(len(pathsEnds)>0):
                minNode = min(pathsEnds, key = lambda x:Cost(x))
                path = getPathToGoal(minNode)
                vis.path = path
        else:
            if not printed:
                printed = True
                print("time to Execute:",n,time.time() - start_time)
            vis.update()
        #pygame.display.flip()
