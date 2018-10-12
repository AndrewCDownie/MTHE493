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
        self.flag = False

    """
    prints the x and y coordinate and all the edges
    """
    def printData(self):
        print("x:"+str(self.x))
        print("y:"+str(self.y))
        print("edges:")
        for next in self.connected:
            print("("+str(self.x)+", "+str(self.y)+")->("+ str(next.x)+", "+str(next.y)+")")
    

"""
links nodes by adding each node to each other edges
"""
def linkNodes(node1, node2):
    node1.connected.append(node2)
    node2.connected.append(node1)

