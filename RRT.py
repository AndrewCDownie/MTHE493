#RRT
from Node import *
from Obstacle import *
#from visulization import *
import scipy as sc
import math
import time
root = Node(10,10)
goal = (0,0)

def distToPoint(node1, p,p2p = False):
    if(p2p):
        #if gsetting distance between 2 points
        return math.sqrt((node1[0]-p[0])**2 + (node1[1]-p[1])**2)
    return math.sqrt((node1.x-p[0])**2 + (node1.y-p[1])**2)

def distNodeToNode(node1,node2):
    return math.sqrt((node1.x-node2.x)**2 + (node1.y-node2.y)**2)


"""
Finds the near point in the tree to a given point
Params:
treeRoot: root of the tree to search through
point: coordinate of point wanting to find the nearest node
return node in tree that is closest to it
"""
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

"""
params
TreeRoot: root of Tree
Point: point coordinate (x,y)want that you want to find the nodes in the tree with in a radius of that point
r: radius around the point to find nodes within
"""
def Near(treeRoot,point,r):
    nearNodes = []
    queue = [treeRoot]
    while len(queue)>0:
        node = queue.pop(0)
        if(distToPoint(node,point)<r):
            nearNodes.append(node)
        for child in node.connected:
            queue.append(child)
    return nearNodes

"""
params
point: coordinate of point (x,y)
returns cost of that point given a cost function
"""

def Cost(node_):
    #to be implemented later
    node = node_
    cost = 0
    if node.parent is None:
        return 0
    while node.parent.parent is not None:
        cost += CostOfEdge(node,node.parent) +distToPoint(node,goal)
        node = node.parent
    return cost

def CostOfEdge(node1,node2):
    #return distToPoint(node1,goal)+ distNodeToNode(node1,node2)
    return  distNodeToNode(node1,node2)
    #return distToPoint(node2,goal)

"""
Samples a point in space giving a unifom distribution
returns a point that is not inside of an object
"""

def SampleFree():
    # check new xy to see if it is free
    x = (sc.random.uniform(0, 500))
    y = (sc.random.uniform(0, 500))
    numObs = len(obstalce_list)

    for obj in obstalce_list:
        while obj.checkInside((x,y)):
            x = int(sc.random.uniform(0, 500))
            y = int(sc.random.uniform(0, 500))



    # Make sure this isn't in an obstaclc
    return (x,y)

def collisionFree(node,point):
    for obs in obstalce_list:
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
def steer(node, point):
    N = 10
    L = math.sqrt((point[0]-node.x)**2 + (point[1]-node.y)**2)
    if L<N:
        return point
    vect = (node.x+(N/L)*(point[0]-node.x),node.y+(N/L)*(point[1]-node.y))
    return vect

""""
checks if there is a obstacle between the node ane the point

"""
def obstacleFree(node,point):
    for obs in obstalce_list:
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
        path.append(curNode)
        curNode = curNode.parent
    path.append(curNode)
    return path

        

def RRT(root,finish,acc):
    n = 1
    newNode = root
    #time.sleep(0.05)
    #while distToPoint(newNode,finish) > acc:
    x= 0
    while x < 8000:
        x+=1
        randPoint = SampleFree()
        nearest = Nearest(root,randPoint)
        newPoint = steer(nearest,randPoint)
        if(obstacleFree(nearest,newPoint)):
            newNode = Node(newPoint[0],newPoint[1])
            nearest.addChild(newNode)

    return root, getPathToGoal(newNode)


def RRTStar(root,finish,acc):
    goal = finish
    xNewNode = root
    eta = 10
    x = 1
    #while distToPoint(xNewNode,finish)> acc and x <1000:
    while x <11000:
        x+=1
        xRand = SampleFree()
        xNearest = Nearest(root,xRand)
        xNew = steer(xNearest,xRand)
        if obstacleFree(xNearest,xNew):
            cMin = 0
            xNewNode = Node(xNew[0],xNew[1])
            ##need to add Card(V)
            cardV = 50
            NearPoints = Near(root,xNew,min(eta,cardV))
            xMin = xNearest 
            cMin = Cost(xNearest)+ CostOfEdge(xNearest,xNewNode)
            for xNear in NearPoints:
                if(collisionFree(xNear,xNew)and Cost(xNear) + CostOfEdge(xNear,xNewNode)<cMin):
                    xMin = xNear
                    cMin = Cost(xNear) + CostOfEdge(xNear,xNewNode)
            xMin.addChild(xNewNode)
            for xNear in NearPoints:
                if collisionFree(xNear,(xNewNode.x,xNewNode.y)) and Cost(xNewNode)+ CostOfEdge(xNear,xNewNode)< Cost(xNear):
                    xParent = xNear.parent
                    xNewNode.addChild(xNear)
                    xParent.connected.pop(xParent.connected.index(xNear))
    print("my root")
    print(root)                    
    return root 
        



obj = obstacle([(100,100),(200,150),(200,200),(150,200)])
obstalce_list = [obj]
