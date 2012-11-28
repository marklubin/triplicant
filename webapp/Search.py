"""
Search.py: class for peforming graph seach on locations
Mark Lubin
"""
from Location import Locations

class Search:
    def __init__(self):
        self._locations = Locations()#intialize collection of locations

        self._pathCosts = {}#cache for path costs
        for loc in self._locations:
            self._pathCosts[loc] = {}

    def getSearchLocations(self):#return a dict with location information, so the client can give us endpoints
        return self._locations.getLocations()

    def computePath(self,l1,l2):pass #actual A* search


    def pathCost(loc1,loc2,heuristic): pass #compute pathcost between two locations

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






if __name__ == '__main__':
    cliTest()
