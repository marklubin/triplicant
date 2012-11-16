
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from itertools import cycle


###############################################################################
# Generate sample data
#centers = [[1, 1], [-1, -1], [1, -1]]
#X, _ = make_blobs(n_samples=10000, centers=centers, cluster_std=0.6)
#import pdb; pdb.set_trace()
###############################################################################
# Compute clustering with MeanShift

# The following bandwidth can be automatically detected using
#bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=500)

def cluster():
    bandwidth = .1#about 70*bandwidth in  miles
    cluster_limit = 75
    dpi = 400
    f = open("platlong.csv")
    f.readline()#skip for line
    X = []
    for line in f.readlines():
        X.append([float(coord )for coord in line.split(',')])
        X = np.array(X)

        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True,\
                       cluster_all = False)
        ms.fit(X)
        labels = ms.labels_
        cluster_centers = ms.cluster_centers_

        labels_unique = np.unique(labels)
        n_clusters_ = len(labels_unique)

        print "number of estimated clusters : %d" % n_clusters_

###############################################################################

def clusterPlot(bandwidth,cluster_limit,labels,cluster_centers\
                ,n_clusters,labels_unique):
    fig = plt.figure(figsize=(8,4),dpi = 200)
    fig.add_subplot(1,1,1)

    # llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
    # are the lat/lon values of the lower left and upper right corners
    # of the map.
    # lat_ts is the latitude of true scale.
    # resolution = 'c' means use crude resolution coastlines.
    m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=75,\
                llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='i')
    m.drawcoastlines(linewidth=.05)
    m.drawcountries(linewidth=.05)


    accepted_clusters = 0
    colors = cycle('bgrcmybgrcmybgrcmybgrcmy')
    for k, col in zip(range(n_clusters_), colors):
        my_members = labels == k
        cluster_size = len(X[my_members,0])
        if cluster_size < cluster_limit: continue
        accepted_clusters += 1
        cluster_center = cluster_centers[k]
        pairs = [(X[my_members, 0], X[my_members, 1])\
                 ,(cluster_center[0], cluster_center[1])]
        coords = [m(y,x) for x,y in pairs]
        plt.plot(coords[0][0], coords[0][1], col \
                 , marker = ',', markersize = .05)
        plt.plot(coords[1][0], coords[1][1], 'o'\
                 , markeredgecolor='k', markersize=.05)

        plt.title('Estimated number of clusters: %d Bandwidth:\
        %.1f degrees of latitude \n Noise Threshold %d'\
        % (accepted_clusters,bandwidth,cluster_limit)\
        ,fontsize = 12)


        plt.savefig("clustered.png",dpi = 200)


if __name__ == '__main__':
    cluster()
