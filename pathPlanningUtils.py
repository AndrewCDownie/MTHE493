import math
import scipy as sc
import time
from Node import *
from Obstacle import *
from BinHeap import BinHeap
import numpy as np
def distToPoint(node1, p,p2p = False):
    if(p2p):
        #if gsetting distance between 2 points
        return math.sqrt((node1[0]-p[0])**2 + (node1[1]-p[1])**2)
    return math.sqrt((node1.x-p[0])**2 + (node1.y-p[1])**2)

def distNodeToNode(node1,node2):
    return math.sqrt((node1.x-node2.x)**2 + (node1.y-node2.y)**2)

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

def Cost(node_,state):
    #to be implemented later
    if node_.cost != 0:
        return node_.cost
    node = node_
    cost = 0
    if node.parent is None:
        return 0
    while node.parent.parent is not None:
        cost += CostLI(node,node.parent,state) 
        node = node.parent

    node_.cost = cost
    return cost


def CostOfEdge(node1,node2):
    #return distToPoint(node1,goal)+ distNodeToNode(node1,node2)
    return  distNodeToNode(node1,node2)
    #return distToPoint(node2,goal)


"""
Samples a point in space giving a unifom distribution
returns a point that is not inside of an object
"""

def SampleFree(obstacleL,dims):
    # check new xy to see if it is free
    x = (sc.random.uniform(0, dims[0]))
    y = (sc.random.uniform(0, dims[1]))

    for obj in obstacleL:
        while obj.checkInside((x,y)):
            x = (sc.random.uniform(0, dims[0]))
            y = (sc.random.uniform(0, dims[1]))



    # Make sure this isn't in an obstaclc
    return (x,y)

def collisionFree(node,point, obstacleL):
    for obs in obstacleL:
        #check if point is a Node
        if(type(point) == Node):
            point = (point.x,point.y)

        if(obs.checkPassThrough((node.x,node.y),point)):
            return False
    return True
"""
takes sampled point and a node and creates a vector from node pointing towards the sampled point of length N
params:
node: node in the tree to steer from 
point: point (x,y) to steer too
returns: point (x,y) that is end of vector from node

"""
def steer(node, point, eta):
    N = eta
    L = math.sqrt((point[0]-node.x)**2 + (point[1]-node.y)**2)
    if L<N:
        return point
    vect = (node.x+(N/L)*(point[0]-node.x),node.y+(N/L)*(point[1]-node.y))
    return vect

""""
checks if there is a obstacle between the node ane the point

"""
def obstacleFree(node,point,obstacleL):
    for obs in obstacleL:
        if obs.checkPassThrough((node.x,node.y), point):
            return False

    return True


"""
gets a path from the beginning 
param:
lastNode: endpoint that hits goal
returns path from start to end point
"""
def getPathToGoal(lastNode):
    curNode = lastNode
    path = [curNode]
    while(curNode.parent is not None):
        path.insert(0,curNode)
        curNode = curNode.parent
    path.insert(0,curNode)
    
    return path


"""
FMT FUNCTIONS
"""

def SampleFreeN(n,obs,size):
    samples = []
    for i in range(n):
        p = SampleFree(obs,size)
        samples.append(Node(p[0],p[1]))
    return samples

def MemoNear(V,z,r_z,state):
    if z.saved == True:
        return z.near
    else:
        for v in V:
            if(z is v):
                pass
            elif CostLI(z,v,state) < r_z :
                z.near.append(v)
        z.saved = True
        return z.near


def getRz():
    #to be coded
    return 15


#returns set of that is  weather it is open or closed
def getOpen(heap,V):
    openV = []
    for v in V:
        if v in heap.heapList:
            openV.append(v)
    return openV

#returns visited or unvisited node based on visited var
def getVisited(V,visited = False):
    visitedV = []
    for v in V:
        if v.visited == visited:
            visitedV.append(v)
    return visitedV

def setOpen(heap,V):
    for v in V:
        heap.insert(v)
    return

#line intergral cost to replace the original on also MEMONEar need to be changed 
def CostLI1(n1,n2,state):
    refinement = 3
    distN2N = distNodeToNode(n1,n2)
    #line space between each point
    x_s = np.linspace(n1.x,n2.x,num = refinement)
    y_s = np.linspace(n1.y,n2.y,num = refinement)
    points = zip(x_s,y_s)
    #summation intergral
    value = 0
    dx = distN2N/refinement
    for point in points:
        value += 1*dx + state.getPointCost(point)*dx #x+ list(points).index(point)*dx#add extra value here from state
    return value

def CostLI(n1,n2,state):
    refinement = 3
    distN2N = distNodeToNode(n1,n2)
    #line space between each point
    x_s = np.linspace(n1.x,n2.x,num = refinement)
    y_s = np.linspace(n1.y,n2.y,num = refinement)
    points = zip(x_s,y_s)
    #summation intergral
    value = distN2N
    dx = distN2N/refinement
    for point in points:
        value += state.getPointCost(point)*dx #x+ list(points).index(point)*dx#add extra value here from state
    return value
    
def sampleRadius(r,point,state):
    #Sample based on density
    samples = []
    while(len(samples)<=100):
        sample = SampleFree(state.obstacles,state.size)
        if distToPoint(point,sample, p2p=True) < r:
            samples.append(Node(sample[0],sample[1]))
    return samples
        


