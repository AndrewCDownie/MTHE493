#node Object

class node(object):
    """
    x_ : x coordinate in the graph
    y_ : y coordinate in the graph
    Node flag is false initally  and edges are empty

    """
    def __init__(self,x_,y_):
        self.x = x_
        self.y = y_
        self.edges = []
        self.flag = False

    """
    prints the x and y coordinate and all the edges
    """
    def printData(self):
        print("x:"+str(self.x))
        print("y:"+str(self.y))
        print("edges:")
        for edge in self.edges:
            print("("+str(self.x)+", "+str(self.y)+")->("+ str(edge.x)+", "+str(edge.y)+")")
    

"""
links nodes by adding each node to each other edges
"""
def linkNodes(node1, node2):
    node1.edges.append(node2)
    node2.edges.append(node1)

