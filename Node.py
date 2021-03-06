#node Object

class Node(object):
    """
    x_ : x coordinate in the graph
    y_ : y coordinate in the graph
    Node flag is false initally  and edges are empty

    """
    def __init__(self,x_,y_):
        self.x = x_
        self.y = y_
        self.connected = []
        self.saved = False
        self.visited = False
        self.open = False
        self.closed = False
        self.parent = None
        self.near = []
        self.cost = 0

    """
    prints the x and y coordinate and all the edges
    """
    def printData(self):
        print("x:"+str(self.x))
        print("y:"+str(self.y)) 
        print("edges:")
        for next in self.connected:
            print("("+str(self.x)+", "+str(self.y)+")->("+ str(next.x)+", "+str(next.y)+")")
    
    def printCoordinate(self):
        print("("+str(self.x)+ ", "+ str(self.y)+")")
    
    def setFlag(self,val):
        self.flag = val

    def addChild(self,childNode):
        self.connected.append(childNode)
        childNode.parent = self

    def getPoint(self):
        return (self.x,self.y)

    def setCost(self,costToNode):
        parentCost = self.parent.cost
        self.cost = costToNode + parentCost
"""
links nodes by adding each node to each other edges
"""
def linkNodes(node1, node2):
    node1.connected.append(node2)
    node2.parent = node1
    #return node1, node2

