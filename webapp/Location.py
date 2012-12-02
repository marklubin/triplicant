"""
Location.py: Class representation of a location from database
Mark Lubin
"""

import psycopg2
import secret

class Locations:#collection of Location
    def __init__(self):

        #initalize a list of locations
        self.locations = {}
        cn = psycopg2.connect(secret.DB_CONNECT)
        cr =  cn.cursor()
        cr.execute("SELECT location_id, latitude, longitude, placename, importance FROM Locations")

        for lid,lat,lon,name,imp in cr.fetchall():
            self.locations[lid] = Location(lid,(float(lat),float(lon)),name,float(imp))

    def __iter__(self):
        for lid in self._locations:
            yield self._locations[lid]
            
    def asIds(self):
      return self.locations.keys()


    def getLocations(self):
        locs = {}#dictionary of location information
        for loc in self.locations:
            latlong = self.locations[loc].getLatLong()
            name = self.locations[loc].getPlacename()
            locs[loc] = {"id"       : loc,
                         "latitude" : latlong[0],
                         "longitude": latlong[1],
                         "name"     : name}
        return locs


    def successorsForLocation(self,lid):
        #successors = self._locations.keys()[:]
        #successors.remove(lid)
        #return successors
        if not lid in self.locations.keys():
            raise LocatiionError("No location for ID: %d" % lid)
        return self._locations[lid].getSuccessors()

    def placenameForLocation(self,lid):
        if not lid in self.locations.keys():
            raise LocatiionError("No location for ID: %d" % lid)
        return self.locations[lid].getPlacename()

    def coordsForLocation(self,lid):
        if not lid in self.locations.keys():
            raise LocatiionError("No location for ID: %d" % lid)
        return self.locations[lid].getLatLong()

    def importanceForLocation(self,lid):
        if not lid in self.locations.keys():
            raise LocatiionError("No location for ID: %d" % lid)
        return self.locations[lid].getImportance()




class Location:

    def __init__(self,loc_id,latlong,placename,importance):#build a new location given this id num
        self._latlong = latlong
        self._placename = placename
        self. _loc_id = loc_id
        self._importance = importance
        self._successors = []


    def getLatLong(self): return self._latlong

    def getPlacename(self): return self._placename

    def getImportance(self): return self._importance

    def getSuccessors(self):
        if not self._successors:#load up the list on the fly if we need it
            cn = psycopg2.connect(secret.DB_CONNECT)
            cr = cn.cursor()
            cr.execute("SELECT dest_id FROM edges WHERE source_id = (%s) AND prob > 0.0",(self._loc_id,))
            [self._successors.append(row[0]) for row in cr.fetchall()]
        return self._successors

    def __str__(self):
        return "Location Number: %d \n\
                at %f,%f \n\
                name: %s \n\
                I = %f" % (self._loc_id,self._latlong[0],self._latlong[1],self._placename,self._importance)


class LocationError(Exception):
    def __init_(self,location):
        self.lerror = lerror

    def __str__(self):
        return repr(self.lerror)

if __name__ == '__main__':
    locs = Locations()
    for loc in locs:
        print str(loc) + "\n\n" + str(loc.getSuccessors())
