import pygame
import random
from Node import *
from Obstacle import *
from RRT import *
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
        
        self.lines = []
        self.nodes = []
        self.obtacles = []
        self.path = []
        self.root = None

    def drawLines(self,colour):
        for line in self.lines:
            pygame.draw.line(self.display,colour,line['start'],line['end'])
        
    def drawObstacles(self):
        for elem in self.obtacles:
            pygame.draw.polygon(self.display, self.BLACK, elem.points, 0)

    def drawEdges(self,node):
        for next in node.connected:
            pygame.draw.line(self.display,self.GREEN,(node.x,node.y),(next.x,next.y),2)

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
        pygame.draw.circle(self.display, self.BLACK, (200,500), 10,2)
        pygame.display.flip()

running  = True

vis = visualization((500,500))

root = Node(100,100)

root,path = RRT(root,(200,500))

vis.path = path

vis.root = root

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    vis.update()
    #pygame.display.flip()


