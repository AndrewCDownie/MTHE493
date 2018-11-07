#RRT
from Node import *
from Obstacle import *
#from visulization import *
import scipy as sc
import math
import time
root = Node(10,10)

def distToPoint(node1, p):
    return math.sqrt((node1.x-p[0])**2 + (node1.y-p[1])**2)

def Nearest(treeRoot, point):
    nearest = treeRoot
    minDist = distToPoint(treeRoot,point)
    queue = [treeRoot]
    while len(queue)>0:
        node = queue.pop(0)
        dist = distToPoint(node,point)
        if minDist>dist:
            minDist = dist
            nearest = node
        for child in node.connected:
            queue.append(child)
    return nearest

def SampleFree():
    # check new xy to see if it is free
    x = sc.random.uniform(0, 500)
    y = sc.random.uniform(0, 500)
    numObs = len(obstalce_list)

    for num in range(0,numObs+1):
        while obstalce_list[num].checkInside(x,y):
             x = sc.random.uniform(0, 500)
             y = sc.random.uniform(0, 500)
             num = 0


    # Make sure this isn't in an obstaclc
    return (x,y)

def steer(node, point):
    N = 5
    L = math.sqrt((point[0]-node.x)**2 + (point[1]-node.y)**2)
    vect = (node.x+(N/L)*(point[0]-node.x),node.y+(N/L)*(point[1]-node.y))
    return vect

def obstacleFree(node,point):
    for obs in obstalce_list:
        if obs.checkPassThrough(node, point):
            return False

    return True


p = (0,200)

node1 = Node(0,0)
node2 = Node(0,100)
node3 = Node(100,1)
node4 = Node(0,199)


linkNodes(node1,node2)
linkNodes(node2,node3)
linkNodes(node2,node4)

node6= Nearest(node2,p)
node6.printData()

#main Algoithm
def getTree(root, finish):
    n = 1
    for i in range(5000):
        newPoint = SampleFree()
        nearest = Nearest(root,newPoint)
        newPoint = steer(nearest,newPoint)
        newNode = Node(newPoint[0],newPoint[1])
        linkNodes(nearest,newNode)

    return root

def getPathToGoal(lastNode):
    curNode = lastNode
    path = [curNode]
    while(curNode.parent is not None):
        path.append(curNode)
        curNode = curNode.parent
    path.append(curNode)
    return path

        

def RRT(root,finish,acc):
    n = 1
    newNode = root
    time.sleep(0.05)
    while distToPoint(newNode,finish) > acc:
        randPoint = SampleFree()
        nearest = Nearest(root,randPoint)
        newPoint = steer(nearest,randPoint)
        if(obstacleFree(nearest,n)):
            newNode = Node(newPoint[0],newPoint[1])
            nearest.addChild(newNode)
    
    return root, getPathToGoal(newNode)

def RRTStar(root,finish,acc):
    newNode = root
    while distToPoint(newNode,finish)> acc:
        randPoint = SampleFree()
