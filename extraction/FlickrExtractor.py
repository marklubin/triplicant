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
                    placename VARCHAR(100));")

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

        for k in range(0,n_clusters-1):
            my_members = labels == k
            #insert the new location
            if len(locs_np[my_members,0]) < noise: continue
            cr.execute("INSERT INTO locations(location_id,latitude,longitude)\
                        VALUES ((%s),(%s),(%s));"\
                        ,(k,cluster_centers[k][0],cluster_centers[k][1]))
            #update join table
            for pair in zip(locs_np[my_members,0],locs_np[my_members,1]):
                cr.execute("INSERT INTO locationsPhotos(location_id,photo_id)\
                           VALUES ((%s),(%s));",\
                           (k,photo_ids[str(pair[0]) + str(pair[1])]))
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

       #get all the owners
       cr.execute("SELECT DISTINCT owner FROM photos;")
       ownerCnt = 0

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
                  trip.append(photo[2])
                  currentLoc = photo[2]
                  #just pass over photos that stay in currentLoc

           if(len(trip) > 1):#this owner saw more than one location
                cr.execute("INSERT INTO owners(flickr_id,journey)\
                            VALUES (%s,%s);",(owner[0],json.dumps(trip)))
       cn.commit()
       cn.close()

    """compute the importance vector"""
    def solve():
        pass


if __name__ == '__main__':
    flickr = FlickrExtractor()
    flickr.computeOwnerJourneys()
    #flickr.locationMake(.5,100)
