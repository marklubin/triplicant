"""
FlickrExtractor.py : A class with methods for dealing with data from the Flickr
API and processing data.
"""
import sqlite3
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
        cn = sqlite.connect("triplicant.db")
        cn.execute("DROP TABLE IF EXISTS locations")
        cn.execute("DROP TABLE IF EXISTS locationPhotos")

        #make them anew
        cn.execute("CREATE TABLE locations (\
                    location_id INTEGER PRIMARY KEY,\
                    latitude FLOAT,
                    longitude FLOAT,
                    placename VARCHAR(100));")

        cn.execute("CREATE TABLE locationPhotos(\
                    lp_id INTEGER PRIMARY KEY,\
                    location_id INTEGER,\
                    photo_id INTEGER);")

        locs = []
        photo_ids = {}
        #get a list of the photo locations
        for row in cn.execute("SELECT latitude,longitude,photo_id FROM photos"):
            locs.append([row[0],row[1])#build up matrix
            photo_ids[str(row[0]) + str(row[1])] = row[2]#save the id for later

        locs_np = np.array(locs)#numpy array

        clusterer = MeanShift(bandwidth = bandwidth, bin_seeding = True,\
                              cluster_all = False)#compute meanshift

        #TODO extract data clusters and label photos with clusters




    """compute each user path and the markov model probabilities, store in db"""
    def computeUserTripsAndProbablities(self):
        pass

    """compute the importance vector"""
    def solve():
        pass

    def makeTestSet(self,size):#create a subset of the big database for testing

if __name__ == '__main__':
    pass
