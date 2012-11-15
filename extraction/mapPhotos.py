from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8,4),dpi = 4000)
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
#m.fillcontinents(color='gray',lake_color='white')
# draw parallels and meridians.
#m.drawparallels(np.arange(-90.,91.,30.))
#m.drawmeridians(np.arange(-180.,181.,60.))
#m.drawmapboundary(fill_color='black')
plt.title("Photo Distribution")

f = open("platlong.csv","r")#input file
f.readline()#skip first line
points = []
for line in f.readlines():
	lat,lon = [float(x) for x in line.split(',')]#extract coords
	points.append(tuple(m(lon,lat)))
x,y = zip(*points)
#plt.plot(x,y)
plt.scatter(x,y,s= .1,marker='.',c='red',edgecolors='none')
plt.savefig("superdetailed.png",dpi = 4000)

	
	
	
#plt.show()