import math
class obstacle(object):

    def __init__(self,points_):
        self.points = list(points_)
                
    def checkInside(self,point):
        #Append to self points the point 
        copy=self.points
        copy.append(point)
        minYP = min(copy, key = lambda x:x[1])
        def polarAngle(p):
            px = p[0]-minYP[0]
            py = p[1]-minYP[1]
            return math.atan2(py,px)
        sortedByPolar = sorted(copy, key = polarAngle)
        lengthof=len(sortedByPolar)
        flag=0
        secondlast=sortedByPolar[lengthof-2]
        last=sortedByPolar[lengthof-1]
        firstcheck=sortedByPolar[0]
        secondcheck=sortedByPolar[1]
        if 0>=((last[0]-secondlast[0])*(firstcheck[1]-secondlast[1]))-((firstcheck[0]-secondlast[0])*(last[1]-secondlast[1])):
            flag=1
        if 0>=((firstcheck[0]-last[0])*(secondcheck[1]-last[1]))-((secondcheck[0]-last[0])*(firstcheck[1]-last[1])):
            flag=1
        for i in range(2,len(sortedByPolar)):
            first=sortedByPolar[i-2]
            second=sortedByPolar[i-1]
            third=sortedByPolar[i]
            val=((second[0]-first[0])*(third[1]-first[1]))-((third[0]-first[0])*(second[1]-first[1])) 
            #Right Turn or colinear
            if val<=0:
                flag=1
        if flag==1:
            return True
        else:
            return False

    def checkPassThrough(self,point1,point2):
        slopepoints=(point2[1]-point1[1])/(point2[0]-point1[0])
        b1=point2[1]-slopepoints*point2[0]
        for i in range (1,len(self.points)):
            first=self.points[i+1]
            second=self.points[i]
            slopeself=(second[1]-first[1])/(second[0]-first[0])
            b2=second[1]-slopeself*second[0]
            xintersect=(b1-b2)/(slopepoints-slopeself)
            if xintersect>=first[0] and xintersect<=second[0]:
                return True
        return False

    def printPoints(self):
        for elem in self.points:
            print("("+str(elem[0])+", "+str(elem[1])+")")


obj1 = obstacle([(0,0),(1,0),(1,1),(0,1)])

obj1.printPoints()
if obj1.checkInside((1.5,0.5))==True:
    print('True')
else:
    print('False')