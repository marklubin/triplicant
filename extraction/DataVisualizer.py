"""
DataVisualizer.py: Class for visualizing the flickr data
Mark Lubin
"""
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import psycopg2
from time import time
from itertools import cycle
import secret

class DataVisualizer:
    def __init__(self):
        pass


    """map a table that has lat,long columns"""
    def mapMake(self,renderdpi,table,msize):
        cn = 0
        start = time()

        #initialize connection to database
        cn = psycopg2.connect(secret.DB_CONNECT)
        cr = cn.cursor()

        #get map ready to go
        fig = plt.figure(figsize=(8,4),dpi = renderdpi)
        fig.add_subplot(1,1,1)
        m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=75,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='i')
        m.drawcoastlines(linewidth=.05)
        m.drawcountries(linewidth=.05)

        photoCnt = 0
        points = []

        cr.execute('SELECT latitude,longitude FROM %s;' %  table)
        for row in cr.fetchall():
            x,y = m(row[1],row[0])#convert to merc projection coords
            points.append((x,y))
            photoCnt += 1
        xs,ys = zip(*points)

        plt.title("%d %s" % (photoCnt,table))
        plt.scatter(xs,ys,s=msize,marker='.',c='green',edgecolors='none')
        plt.savefig(table,dpi = renderdpi)

        print "{:d} {:s}  mapped in {:f} seconds".format(photoCnt,\
                                                         table,time()-start)


    """Make a map with paths  of user trips"""
    def ownerTripsMapMake(self,renderdpi,filename,lwidth):
        cn = 0
        start = time()

        #initialize connection to database
        cn = psycopg2.connect(secret.DB_CONNECT)
        cr = cn.cursor()

        #get map ready to go
        fig = plt.figure(figsize=(8,4),dpi = renderdpi)
        fig.add_subplot(1,1,1)
        m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=75,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='i')
        m.drawcoastlines(linewidth=.05)
        m.drawcountries(linewidth=.05)

        photoCnt = 0
        points = []

        #get a dictionary mapping of locations idea to lat,longs
        cr.execute('SELECT location_id,latitude,longitude FROM locations;')
        locations = {}
        for row in cr.fetchall():locations[row[0]] = (row[1],row[2])

        #iterate through owners
        cr.execute('SELECT journey FROM owners;')
        import json
        userCnt = 0
        colors = cycle('bgrckmybgrckmybgrckmybgrckmy')
        for row,col  in zip(cr.fetchall(),colors):
            userCnt += 1
            journey = json.loads(row[0])
            points = []
            for loc in journey:#get an list of the x,y points
                latlong = locations[loc]
                points.append((m(latlong[1],latlong[0])))
            x,y = zip(*points)
            plt.plot(x,y,color = col,linewidth = lwidth)

        plt.savefig(filename,dpi = renderdpi)

        print "Rendered in {:f} seconds".format(time()-start)



if __name__ == '__main__':
    #TODO allow command line arguments to produce maps on fly
    dv = DataVisualizer()
    #dv.mapMake(1000,"locations",2)
    dv.mapMake(300,"photos",.1)
    dv.mapMake(300,"locations",10)
    dv.ownerTripsMapMake(300,'trips',.01)
