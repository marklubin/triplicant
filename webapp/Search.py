"""
Search.py: class for peforming graph seach on locations
Mark Lubin
"""
from Location import Locations
import Queue
from math import acos,sin,cos,radians
from datetime import timedelta

RADIUS = 6368 #radius of earth in kilometers
TRAVEL_RATE = .02682 #km/s = 60 mph
DAY = timedelta(days = 1).total_seconds()
MAX_TIME_IN_LOCATION = timedelta(days = 5).total_seconds()


class Search:
    def __init__(self):
        self._locations = Locations()#intialize collection of locations

        self._pathCosts = {}#cache for path costs
        for loc in self._locations:
            self._pathCosts[loc] = {}

    def getSearchLocations(self):#return a dict with location information, so the client can give us endpoints
        return self._locations.getLocations()

    def computePath(self,l1,l2,travelTime,h = lambda x:0): #A* search
        print travelTime
        h = lambda x: self.pathCost(x,l2)[1]
        openSet = Queue.PriorityQueue()
        closedSet =  []
        i = self._locations.importanceForLocation(l1)
        openSet.put((0,Node(l1,0,0,i,0)))
        goalNode = 0


        while not openSet.empty():#while this isn't the destination
            curr = openSet.get()[1]
            loc = curr.nid
            cost = curr.cost
            if loc == l2:#goal reached record this node so we can find path
                print curr.time
                if goalNode and curr.time > travelTime:#we return the last possible path that is under the time limite
                    break
                else:
                    goalNode = curr
                    print "Goal reachable with score %f in %f" % (goalNode.score,goalNode.time)
            if loc not in closedSet:
                closedSet.append(loc)
                for successor in self._locations.successorsForLocation(loc):
                    importance = self._locations.importanceForLocation(successor)
                    c ,time = self.pathCost(loc,successor)
                    score = importance + curr.score
                    time += curr.time
                    weight = c + + cost +  h(successor)
                    node = Node(successor,c,curr,score,time)
                    openSet.put((c,node))

        #unweave the path
        path = []
        node  = goalNode

        nodes = []
        while node:
            path.append(node.nid)
            nodes.append(node)
            node  = node.parent

        nodes.reverse()

        for node in nodes:
            print "To %s in %f seconds with score %f" % (self._locations.placenameForLocation(node.nid),node.time,node.score)
        path.reverse()
        return path


    def pathCost(self,l1,l2):
        d = self.greatCircleDistance(l1,l2)

        time = d / TRAVEL_RATE #how long it would take going 60mph direct, a poor measure but a start
        time = min(time,DAY)#if the travel time is more than a day we assume we can fly in a day
        return time

    def greatCircleDistance(self,l1,l2):#great circle distance in km
        c1 = [radians(c) for c in self._locations.coordsForLocation(l1)]
        c2 = [radians(c) for c in self._locations.coordsForLocation(l2)]

        dLong = abs(c1[1] - c2[1]) #difference in longitude

        dAngle = acos(sin(c1[0]) * sin(c2[0])
                    + cos(c1[0]) * cos(c2[0]) * cos(dLong))

        #print self._locations.importanceForLocation(l2)
        return RADIUS * dAngle

    def timeForImportance(self,location_id):pass


class Orienteering(Search):

class Node:

    def __init__(self,nid,cost,parent=0,score=0,time=0):
        self.nid = nid
        self.cost = cost
        self.parent = parent
        self.score = score
        self.time = time








        


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
        print "%3d : %-20s\t\t" % (locations[location]["id"],locations[location]["name"]),
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

    ttime = input("Enter travel time in days: ")
    ttime = float(ttime)
    dt = timedelta(days = ttime).total_seconds()
    print "Computing a path from location: %d to location: %d" % (start,end)
    path = s.computePath(start,end,dt)

    for lid in path:
        print s._locations.placenameForLocation(lid)






if __name__ == '__main__':
    s = Search()
    #print s.computePath(256,266)
    cliTest()
