import pygame
import random
from Node import *
from Obstacle import *
from RRT import *
import time
class visualization(object):

    def __init__(self,size_,root_, target_ = (0,0),accuracy_ = 1, obstacles_ = [], scale_ = 7,name = ""):   
        #Define Colours
        self.BLACK = (  0,   0,   0)
        self.WHITE = (255, 255, 255)
        self.BLUE =  (  0,   0, 255)
        self.GREEN = (  0, 255,   0)
        self.RED =   (255,   0,   0) 
        self.PURPLE =(153,  50, 204)
        self.YELLOW =(255, 255,   0)
        #setting up pygame
        pygame.init()
        self.scale = scale_
        #get size of the space to work with
        self.displaySize = (self.scale*size_[0],self.scale*size_[1])

        #get the proper sizing
        self.display = pygame.display.set_mode(self.displaySize)
        pygame.display.set_caption(name)

        #get the clock for the pygame
        self.clock = pygame.time.Clock()

        #whip the screen initally
        self.display.fill(self.WHITE)

        #the target to begin with
        self.target = target_

        #how close the tree has to get
        self.accuracy = accuracy_

        #list of obstacles
        self.obtacles = obstacles_

        #optimal path
        self.path = []

        self.curPath = []
        
        self.noReroutePath = []

        self.pathToGo = []

        self.travelledPath = []

        self.nodes = [] 

        self.detectedPoints = []

        self.mouseLoc = (0,0)
        #root of the tree

        self.root = root_
        self.robotPos = (0,0)
        self.robotRadius = 20
        self.i = 0
       

    def drawTree(self,root):
        queue = [root]
        while len(queue)>0:
            node = queue.pop(0)
            for child in node.connected:
                queue.append(child)
            self.drawEdges(node)
        
    def drawEdges(self,node):
        for next in node.connected:
            pygame.draw.line(self.display,self.RED,(self.scale*node.x,self.scale*node.y),(self.scale*next.x,self.scale*next.y),3)

    def drawPath(self):
        for i in range(1,len(self.path)):
            pygame.draw.line(self.display,self.BLUE,(self.scale*self.path[i-1].x,self.scale*self.path[i-1].y),(self.scale*self.path[i].x,self.scale*self.path[i].y),7)
    
    def drawNoReroutePath(self):
        for i in range(1,len(self.noReroutePath)):
            pygame.draw.line(self.display,self.BLUE,(self.scale*self.noReroutePath[i-1].x,self.scale*self.noReroutePath[i-1].y),(self.scale*self.noReroutePath[i].x,self.scale*self.noReroutePath[i].y),7)

    def drawCurPath(self):
        for i in range(1,len(self.curPath)):
            pygame.draw.line(self.display,self.GREEN,(self.scale*self.curPath[i-1].x,self.scale*self.curPath[i-1].y),(self.scale*self.curPath[i].x,self.scale*self.curPath[i].y),7)

    def drawPathToGo(self):
        for i in range(1,len(self.pathToGo)):
            pygame.draw.line(self.display,self.GREEN,(self.scale*self.pathToGo[i-1][0],self.scale*self.pathToGo[i-1][1]),(self.scale*self.pathToGo[i][0],self.scale*self.pathToGo[i][1]),7)

    
    def drawTravelledPath(self):
        for i in range(1,len(self.travelledPath)):
            pygame.draw.line(self.display,self.PURPLE,(self.scale*self.travelledPath[i-1][0],self.scale*self.travelledPath[i-1][1]),(self.scale*self.travelledPath[i][0],self.scale*self.travelledPath[i][1]),7)


    def drawObstacles(self):
        for elem in self.obtacles:
            scaleedPoints = []
            for point in elem.rawpoints:
                scaleedPoints.append(( self.scale*point[0],self.scale*point[1]))
            pygame.draw.polygon(self.display, self.BLACK, scaleedPoints, 0)

    def drawNodes(self):
        for n in self.nodes:
            pygame.draw.circle(self.display, self.BLACK, (self.scale*round(n.x),self.scale*round(n.y)),2,1)

    def drawRobot(self):
            pygame.draw.circle(self.display,self.GREEN,(round(self.scale*(self.robotPos[0])),round(self.scale*(self.robotPos[1]))),self.scale*2)
            pygame.draw.circle(self.display,self.BLACK,(round(self.scale*(self.robotPos[0])),round(self.scale*(self.robotPos[1]))),self.scale*self.robotRadius,1)

    def drawDetected(self):
        for detection in self.detectedPoints:
            pygame.draw.circle(self.display, self.PURPLE, (self.scale*detection[0],self.scale*detection[1]),self.scale*4,2)

    def update(self):
        if self.i > 0:
            #whip the screen
            self.display.fill(self.WHITE)
            #print(self.obtacles)
            #draw the black retangles
            self.drawObstacles()

            #draw the tree created
            self.drawTree(self.root)

            #draw the path of the optimal route
            self.drawPath()
            #draw current traversal path
            self.drawPathToGo()

            self.drawNodes()
            self.drawNoReroutePath()
            self.drawTravelledPath()
            #draw the goal -need to fix
            pygame.draw.circle(self.display, self.BLACK, (self.scale*self.target[0],self.scale*self.target[1]),self.scale*self.accuracy,2)
            #update the screen
            self.drawRobot()

            self.drawDetected()

            pygame.display.update(pygame.Rect(0, 0, 10000, 10000))
            self.i = self.i  
            return
        self.i += 1





if __name__ == "__main__":

    scale = 5
    running  = True
    clock = pygame.time.Clock()
    root = Node(0,0)
    vis = visualization((100,100),root)

    

    accuracy = 10
    target = (100,100)

    vis.accuracy = accuracy
    vis.target = target
    vis.path = []
    print(vis.path)
    vis.root = root
    vis.display.fill(vis.WHITE)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #clock.tick(30)

        #root = RRTStar(root,target,accuracy)
        vis.update()
        
        #pygame.display.flip()
        


