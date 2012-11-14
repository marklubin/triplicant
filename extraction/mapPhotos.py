from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# lat_ts is the latitude of true scale.
# resolution = 'c' means use crude resolution coastlines.
m = Basemap(projection='merc',llcrnrlat=-60,urcrnrlat=75,\
            llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
m.drawcoastlines()
#m.fillcontinents(color='gray',lake_color='white')
# draw parallels and meridians.
#m.drawparallels(np.arange(-90.,91.,30.))
#m.drawmeridians(np.arange(-180.,181.,60.))
#m.drawmapboundary(fill_color='black')
plt.title("Photo Distrobution")

f = open("latlong.csv","r")#input file
f.readline()#skip first line
points = []
for line in f.readlines():
	lat,lon = [float(x) for x in line.split(',')]#extract coords
	points.append(tuple(m(lon,lat)))
x,y = zip(*points)
#plt.plot(x,y)
plt.scatter(x,y,marker='.',c='red',edgecolors='none')

	
	
	
plt.show()