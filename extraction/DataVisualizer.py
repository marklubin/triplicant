"""
DataVisualizer.py: Class for visualizing the flickr data
Mark Lubin
"""
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from time import time

DATABASE = "triplicant.db"

class DataVisualizer:
    def __init__(self):
        pass

    """Make a map of the raw flickr data"""
    def rawMapMake(self,renderdpi,filename,msize):
        cn = 0
        start = time()

        #initialize connection to database
        try:
            cn = sqlite3.connect(DATABASE)
        except Exceptions as e:
            print "Error:", e
            return

        #get map ready to go
        fig = plt.figure(figsize=(8,4),dpi = renderdpi)
        fig.add_subplot(1,1,1)
        m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=75,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='i')
        m.drawcoastlines(linewidth=.05)
        m.drawcountries(linewidth=.05)

        s = "SELECT latitude,longitude from photos;"
        photoCnt = 0
        points = []
        for row in cn.execute(s):
            x,y = m(row[1],row[0])#convert to merc projection coords
            points.append((x,y))
            photoCnt += 1
        xs,ys = zip(*points)

        plt.title("%d Flickr Photos" % photoCnt)
        plt.scatter(xs,ys,s=msize,marker='.',c='red',edgecolors='none')
        plt.savefig(filename,dpi = renderdpi)

        print "{:d} photos mapped in {:f} seconds".format(photoCnt,\
                                                          time()-start)

    """Make a map with both raw photo locations and clusters"""
    def clusterMapMake(self,dpi,filename,markersize):
        pass

    """Make a map with paths  of user trips"""
    def userTripsMapMake(self,dpi,filename,linewidth):
        pass


if __name__ == '__main__':
    #TODO allow command line arguments to produce maps on fly
    dv = DataVisualizer()
    dv.rawMapMake(200,'raw',.1)
