import pygame
import random
from Node import *
from Obstacle import *
from RRT import *
import time

class visualization(object):

    def __init__(self,size_):   
        #Define Colours
        self.BLACK = (  0,   0,   0)
        self.WHITE = (255, 255, 255)
        self.BLUE =  (  0,   0, 255)
        self.GREEN = (  0, 255,   0)
        self.RED =   (255,   0,   0) 
    
        #setting up pygame
        pygame.init()
        self.displaySize = size_
        self.display = pygame.display.set_mode(self.displaySize)
        pygame.display.set_caption("RRT*")
        self.clock = pygame.time.Clock()
        self.display.fill(self.WHITE)
        self.target = (0,0)
        self.accuracy = 0
        self.root = None
        self.obtacles = obstalce_list

    def drawTree(self,root):
        queue = [root]
        while len(queue)>0:
            node = queue.pop(0)
            for child in node.connected:
                queue.append(child)
            self.drawEdges(node)
        
    def drawEdges(self,node):
        for next in node.connected:
            pygame.draw.line(self.display,self.GREEN,(scale*node.x,scale*node.y),(scale*next.x,scale*next.y),1)

    def drawPath(self):
        for i, node in enumerate(self.path,1):
            pygame.draw.line(self.display,self.BLUE,(scale*self.path[i-1].x,scale*self.path[i-1].y),(scale*node.x,scale*node.y),3)

    def drawObstacles(self):
        for elem in self.obtacles:
            scaleedPoints = []
            for point in elem.rawpoints:
                scaleedPoints.append(( scale*point[0],scale*point[1]))
            pygame.draw.polygon(self.display, self.BLACK, scaleedPoints, 0)

    def update(self):
        self.display.fill(self.WHITE)
        self.drawTree(self.root)
        self.drawPath()
        self.drawObstacles()
        pygame.draw.circle(self.display, self.BLACK, (scale*self.target[0],scale*self.target[1]),scale*self.accuracy,2)
        pygame.display.update(pygame.Rect(0, 0, 10000, 10000))


if __name__ == "__main__":
    scale = 5
    running  = True
    clock = pygame.time.Clock()
    vis = visualization((scale*100,scale*100))
    root = Node(0,0)

    accuracy = 4
    target = (100,10)

    vis.accuracy = accuracy
    vis.target = target
    vis.path = []
    vis.root = root

    goal = target
    xNewNode = root
    cardV = 1
    eta = 2
    gammaRRT = getGammaRRT(3)
    pathsEnds =[]
    path = []
    minPathNode = Node(1,1)
    acc = accuracy

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #clock.tick(30)
        
        #root = RRTStar(root,target,accuracy)
        eta = (2**(1/2))
        eta = 4
        #print(eta)
        #print(gammaRRT*((math.log(cardV)/(cardV))**(1/2)))
        
        xRand = SampleFree()
        xNearest = Nearest(root,xRand)
        xNew = steer(xNearest,xRand,eta)
        print(distToPoint(xNearest,xNew))
        if obstacleFree(xNearest,xNew):
            cMin = 0
            xNewNode = Node(xNew[0],xNew[1])
            ##need to add Card(V)

            #NearPoints = Near(root,xNew,min(eta,gammaRRT*((cardV/(2**cardV))**(1/2))))
            NearPoints = Near(root,xNew,eta)
            xMin = xNearest 
            cMin = Cost(xNearest)+ CostOfEdge(xNearest,xNewNode)
            for xNear in NearPoints:
                if(collisionFree(xNear,xNew)and Cost(xNear) + CostOfEdge(xNear,xNewNode)<cMin):
                    xMin = xNear
                    cMin = Cost(xNear) + CostOfEdge(xNear,xNewNode)
            xMin.addChild(xNewNode)
            cardV +=1
            print(len(NearPoints))
            for xNear in NearPoints:
                print("Collision Free"+ str(collisionFree(xNear,(xNewNode.x,xNewNode.y))))
                print("CostCondition" + str(Cost(xNewNode)+ CostOfEdge(xNear,xNewNode)< Cost(xNear)))
                if collisionFree(xNear,(xNewNode.x,xNewNode.y)) and Cost(xNewNode)+ CostOfEdge(xNear,xNewNode)< Cost(xNear):
                    print("got here")
                    xParent = xNear.parent
                    xNewNode.addChild(xNear)
                    xParent.connected.pop(xParent.connected.index(xNear))
            if distToPoint(xNewNode,target)< acc:
                print("Adding Node")
                pathsEnds.append(xNewNode)
        if(len(pathsEnds)>0):
            minNode = min(pathsEnds, key = lambda x:Cost(x))
            path = getPathToGoal(minNode)
            vis.path = path
        vis.update()
        #pygame.display.flip()
