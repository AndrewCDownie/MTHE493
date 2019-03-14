from Node import Node

class BinHeap:

    def __init__(self):
        self.heapList = [Node(0,0)]
        self.currentSize = 0

    def percUp(self,i):

        if self.currentSize == 1:
            return
        while i // 2 > 0:
            if self.heapList[i].cost < self.heapList[i // 2].cost:
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp
            i = i // 2

    def insert(self,k):
        self.heapList.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)
    
    def percDown(self,i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i].cost > self.heapList[mc].cost:
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp
            i = mc

    def minChild(self,i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2].cost < self.heapList[i*2+1].cost:
                return i * 2
            else:
                return i * 2 + 1

    def delMin(self):
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def buildHeap(self,listofnodes):
        i = len(listofnodes) // 2
        self.currentSize = len(listofnodes)
        self.heapList = [0] + listofnodes[:]
        while (i > 0):
            self.percDown(i)
            i = i - 1    

