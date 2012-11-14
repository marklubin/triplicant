f = open('flickrdata.txt','r')
out = open('latlong.csv','w')
out.write("lat,long\n")
for line in f.readlines():
	fields = line.split(',')
	lat = fields[2].split(" ")[3]
	lon = fields[3].split(" ")[3]
	out.write("{:s},{:s}".format(lat,lon))
out.close()
