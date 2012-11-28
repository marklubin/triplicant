"""
FlickrExtractor.py : A class with methods for dealing with data from the Flickr
API and processing data.
"""
import psycopg2
import secret
import numpy as np
import json
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs
import DataVisualizer

class FlickrExtractor:
    def __init__(self):
        pass

    """Fetch new unique data from flickr and add to db"""
    def flickFetch(self, limit):
        #TODO add more unique photos
        pass

    """use mean shift clustering to find locations, update db with locations
    and their member photos"""
    def locationMake(self,bandwidth,noise):
        #delete the old tables
        cn = psycopg2.connect(secret.DB_CONNECT)
        cr = cn.cursor()
        cr.execute("DROP TABLE IF EXISTS locations")
        cr.execute("DROP TABLE IF EXISTS locationsPhotos")

        #make them anew
        cr.execute("CREATE TABLE locations (\
                    location_id INTEGER PRIMARY KEY,\
                    latitude FLOAT,\
                    longitude FLOAT,\
                    placename VARCHAR(100),\
                    importance FLOAT);")

        cr.execute("CREATE TABLE locationsPhotos(\
                    lp_id SERIAL PRIMARY KEY,\
                    location_id INTEGER,\
                    photo_id INTEGER);")

        locs = []
        photo_ids = {}
        #get a list of the photo locations
        cr.execute("SELECT latitude,longitude,photo_id FROM photos")
        for row in cr.fetchall():
            locs.append([row[0],row[1]])#build up matrix
            photo_ids[str(row[0]) + str(row[1])] = row[2]#save the id for later

        locs_np = np.array(locs)#numpy array

        clusterer = MeanShift(bandwidth = bandwidth, bin_seeding = True,\
                              cluster_all = False)#meanshift obj

        clusterer.fit(locs_np)

        labels = clusterer.labels_
        cluster_centers = clusterer.cluster_centers_
        labels_unique = np.unique(labels)
        n_clusters = len(labels_unique)

        print "Found %d clusters." % n_clusters

        #import pdb; pdb.set_trace()

        nCls = 0
        for k in range(0,n_clusters-1):
            my_members = labels == k
            #insert the new location
            if len(locs_np[my_members,0]) < noise: continue
            nCls += 1
            cr.execute("INSERT INTO locations(location_id,latitude,longitude)\
                        VALUES ((%s),(%s),(%s));"\
                        ,(k,cluster_centers[k][0],cluster_centers[k][1]))
            #update join table
            for pair in zip(locs_np[my_members,0],locs_np[my_members,1]):
                cr.execute("INSERT INTO locationsPhotos(location_id,photo_id)\
                           VALUES ((%s),(%s));",\
                           (k,photo_ids[str(pair[0]) + str(pair[1])]))
        print "%d usable clusters recorded" % nCls
        cn.commit()
        cn.close()



    """compute each user path and the markov model probabilities, store in db"""
    def computeOwnerJourneys(self):
       cn = psycopg2.connect(secret.DB_CONNECT);
       print "DATABASE CONNECTED"
       cr = cn.cursor()

       #rebuild Users Table
       cr.execute("DROP TABLE IF EXISTS owners;")

       cr.execute("CREATE TABLE owners (\
                   owner_id SERIAL PRIMARY KEY,\
                   flickr_id VARCHAR(50),\
                   journey  VARCHAR(1000));")
       #rebuilt probablities
       cr.execute("DROP TABLE IF EXISTS probablities")

       cr.execute("CREATE TABLE probablities(\
                   prob_id SERIAL PRIMARY KEY,\
                   source_id INTEGER,\
                   dest_id   INTEGER,\
                   prob FLOAT,\
                   num INTEGER);")#stores N(l_i|l_j)
      #get locations and total photos
       cr.execute("SELECT location_id from LOCATIONS")

       print "Getting locations list."

       T = {} #record total number of times a place is visted
       locations = []# list of locations

       for loc_id in cr.fetchall():
           T[loc_id[0]] = 0
           locations.append(loc_id[0])

       print "Initalizing Probablities"
       #build entry to probablities table
       N = {} #N[source][destination] = number of times we go from source to dest
       for source in locations:
           N[source] = {}
           for destination in locations:
               N[source][destination] = 0.
               cr.execute("INSERT INTO probablities(source_id, dest_id,prob,num)\
                           VALUES (%s,%s,%s,%s)",(source,destination,0.0,0))


       #get all the owners
       cr.execute("SELECT DISTINCT owner FROM photos;")
       ownerCnt = 0

       print "Sequencing owner's trips and computing probablities"

       dCnt = 0
       for owner in cr.fetchall():
           ownerCnt += 1
           if not ownerCnt % 50: print ownerCnt
           #get all this owners photos order by date
           cr.execute("SELECT photos.photo_id,photos.datetime,\
                       locationsPhotos.location_id FROM photos,\
                       locationsPhotos WHERE photos.owner = (%s)\
                       AND photos.photo_id = locationsPhotos.photo_id\
                       ORDER BY photos.datetime ASC;",owner)
           currentLoc = -1
           trip = []
           for photo in cr.fetchall():
               #compute the journey
              if photo[2] != currentLoc:#found somewhere new
                  T[photo[2]] += 1 #increment number of times this location is visted
                  trip.append(photo[2])
                  #if this isn't the first photo we must record the trip transition
                  if currentLoc != -1: N[currentLoc][photo[2]] += 1 #increment pseudoprob
                  currentLoc = photo[2]
              #just pass over photos that stay in currentLoc


           cr.execute("INSERT INTO owners(flickr_id,journey) VALUES (%s,%s);",(owner[0],json.dumps(trip)))


       #TODO maybe normalize probablites to remove people who never leave their current location
       print "Recording probablities"
       for source in N:
           for destination in N[source]:
               if N[source][destination] != 0:
                            cr.execute("UPDATE probablities\
                                        SET prob = (%s), num = (%s)\
                                        WHERE source_id = (%s) AND dest_id = (%s);",
                                        (N[source][destination]/float(T[source]),N[source][destination],source,destination))

       cn.commit()
       cn.close()

       """Get location names using reverse geocoder API"""
    def getLocationNames(self):
        import Geocoder
        cn = psycopg2.connect(secret.DB_CONNECT);
        cr = cn.cursor()
        g = Geocoder.Geocoder()

        cr.execute("SELECT latitude,longitude,location_id FROM locations")

        for latlong in cr.fetchall():
            placename = g.reverse(latlong[0:2])
            print placename,latlong[2]
            if len(placename) > 100: placename = placename[0:99]
            cr.execute("UPDATE locations\
                        SET placename = (%s)\
                        WHERE location_id = (%s);",\
                        (placename,latlong[2]))
        cn.commit()
        cn.close()


    """compute the importance vector"""
    def solve(self):
        R = {}#reward for a given location(total number of photos)
        P = {}#probablities
        cn = psycopg2.connect(secret.DB_CONNECT);
        cr = cn.cursor()

        cr.execute("SELECT location_id FROM locations")

        print "Initalizing dataset."
        #load everything we will need into memory
        locations = cr.fetchall()[:]
        for loc in locations:
            lid = loc[0]
            cr.execute("SELECT count(*) FROM locationsPhotos WHERE location_id = (%s)",(lid,))
            R[lid] = cr.fetchone()[0]
            P[lid] = {}

        print "Retrieving probablities."

        cr.execute("SELECT source_id, dest_id,prob FROM probablities WHERE prob != 0.0")

        for s,d,p in cr.fetchall():
            P[s][d] = p

        print "Computing Importance vector via value iteration"

        I = R.copy() #intialize importance vector

        iterCnt = 0
        delta = 9999
        while delta > .0001:
            I1 = {}#new vector to work with
            for location in I.keys():
                #add in reward factor
                I1[location] = R[location]
                for edge in P[location].keys():#sum over all places we could go next
                    I1[location] += I[edge] * P[location][edge]
            delta = I1[0] - I[0]
            iterCnt += 1
            I = I1.copy()

        print "Recording computed importances to database."

        for location in I.keys():
            cr.execute("UPDATE locations\
                        SET importance = (%s)\
                        WHERE location_id = (%s);",(I[location],location))
        cn.commit()
        cn.close()






if __name__ == '__main__':
    #main routine for data processing and visualization
    flickr = FlickrExtractor()
    #dv = DataVisualizer.DataVisualizer()
    #flickr.locationMake(1,160)
    #dv.mapMake(300,"locations",10)
    flickr.getLocationNames()
    #flickr.computeOwnerJourneys()
    #flickr.solve()
    #dv.mapMake(300,"photos",.1)
    #dv.ownerTripsMapMake(300,'trips',.01)
