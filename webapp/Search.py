"""
Search.py: class for peforming graph seach on locations
Mark Lubin
"""
from Location import Locations
import Queue
from math import acos,sin,cos,radians

RADIUS = 6368 #radius of earth in kilometers

class Search:
    def __init__(self):
        self._locations = Locations()#intialize collection of locations

        self._pathCosts = {}#cache for path costs
        for loc in self._locations:
            self._pathCosts[loc] = {}

    def getSearchLocations(self):#return a dict with location information, so the client can give us endpoints
        return self._locations.getLocations()

    def computePath(self,l1,l2,h = lambda x:0): #A* search
        h = lambda x: .4 * self.greatCircleDistance(x,l2)
        openSet = Queue.PriorityQueue()
        closedSet =  []
        openSet.put((0,Node(l1,0)))
        goalNode = 0


        while True:#while this isn't the destination
            curr = openSet.get()[1]
            loc = curr.nid
            cost = curr.cost
            if loc == l2:#goal reached record this not so we can find path
                goalNode = curr
                break
            if loc not in closedSet:
                closedSet.append(loc)
                for successor in self._locations.successorsForLocation(loc):
                    c = self.pathCost(loc,successor) + cost + h(successor)
                    node = Node(successor,c,curr)
                    openSet.put((c,node))

        #unweave the path
        path = []
        node  = goalNode


        #import pdb; pdb.set_trace()

        while node:
            path.append(node.nid)
            node  = node.parent

        path.reverse()
        return path


    def pathCost(self,l1,l2):
        d = self.greatCircleDistance(l1,l2)
        return -1. * self._locations.importanceForLocation(l2)/(d)

    def greatCircleDistance(self,l1,l2):#great circle distance in km
        c1 = [radians(c) for c in self._locations.coordsForLocation(l1)]
        c2 = [radians(c) for c in self._locations.coordsForLocation(l2)]

        dLong = abs(c1[1] - c2[1]) #difference in longitude

        dAngle = acos(sin(c1[0]) * sin(c2[0])
                    + cos(c1[0]) * cos(c2[0]) * cos(dLong))

        #print self._locations.importanceForLocation(l2)
        return RADIUS * dAngle


def cliTest():#basic command line interface for debugging
    s = Search()
    locations = s.getSearchLocations()

    print "______________________________________________________________________________________________________"
    print "                          Welcome to Triplicant, your travel reccomendation engine"
    print "______________________________________________________________________________________________________"

    print "Please select a start and end point using the correspond number of the desired locations\n\n"

    cnt = 0
    for location in locations:
        cnt += 1
        #TODO make print nicer
        print "%3d : %-75s\t\t" % (locations[location]["id"],locations[location]["name"]),
        if not cnt % 2: print ''
    print "\n"

    start = end = 0
    #get start location
    while 1:
        start = input("Enter starting location: ")
        if int(start) not in locations.keys():
            print("No such location, try again.")
            continue
        else:
            start = int(start)
            break


        #get start location
    while 1:
        end = input("Enter ending location: ")
        if int(start) not in locations.keys():
            print("No such location, try again.")
            continue
        else:
            start = int(start)
            break

    print "Computing a path from location: %d to location: %d" % (start,end)
    path = s.computePath(start,end)

    for lid in path:
        print s._locations.placenameForLocation(lid)

class Node:

    def __init__(self,nid,cost,parent=0):
        self.nid = nid
        self.cost = cost
        self.parent = parent






if __name__ == '__main__':
    s = Search()
    #print s.computePath(256,266)
    cliTest()
