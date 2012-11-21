"""
FlickrExtractor.py : A class with methods for dealing with data from the Flickr
API and processing data.
"""
import psycopg2
import secret
import numpy as np
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
    def computeUserTripsAndProbablities(self):
        pass

    """compute the importance vector"""
    def solve():
        passx


if __name__ == '__main__':
    flickr = FlickrExtractor()
    flickr.locationMake(.5,100)
