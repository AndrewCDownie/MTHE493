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
        self.lines = []
        self.nodes = []
        self.obtacles = []
        self.path = []
        self.root = None
        self.sleepTime = 0.1

    def drawLines(self,colour):
        for line in self.lines:
            pygame.draw.line(self.display,colour,line['start'],line['end'])
        
    def drawObstacles(self):
        for elem in self.obtacles:
            pygame.draw.polygon(self.display, self.BLACK, elem.points, 0)

    def drawEdges(self,node):
        for next in node.connected:
            pygame.draw.line(self.display,self.GREEN,(node.x,node.y),(next.x,next.y),1)

    def drawTree(self,root):
        queue = [root]
        while len(queue)>0:
            node = queue.pop(0)
            for child in node.connected:
                queue.append(child)
            self.drawEdges(node)

    def drawPath(self):
        for i, node in enumerate(self.path,1):
            pygame.draw.line(self.display,self.BLUE,(self.path[i-1].x,self.path[i-1].y),(node.x,node.y),3)

    

    def update(self):
        self.display.fill(self.WHITE)
        self.drawLines(self.BLACK)
        self.drawObstacles()
        self.drawTree(self.root)
        self.drawPath()
        pygame.draw.circle(self.display, self.BLACK, self.target, self.accuracy,2)
        pygame.display.update(pygame.Rect(0, 0, 500, 500))
        #time.sleep(self.sleepTime)


running  = True
clock = pygame.time.Clock()
vis = visualization((500,500))

root = Node(0,0)

accuracy = 10
target = (400,400)

vis.accuracy = accuracy
vis.target = target
#root,path = RRT(root,target,accuracy)
root = RRTStar(root,target,accuracy)


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


