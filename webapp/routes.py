"""
routes.py
main entry point for web application
Mark Lubin
"""
DEBUG = False
COMPUTE_TIME = 200

from flask import Flask,url_for,render_template,request
from Location import Locations
from Orienteer import OrienteeringProblem,Tour,Node,greatCircleDistance
import json,time,os
from math import sqrt

maxDetour = lambda x: 40.0/sqrt(x) * x ;#special non-linear function for detour calculation
app = Flask(__name__)#Flask app object
locations = Locations()

def getClosestNode(latLng):
	closest = -1
	closest_dist = 99999.

	for lid in locations.asIds():
		dist = greatCircleDistance(latLng,locations.coordsForLocation(lid))
		if dist < closest_dist:
			closest = lid
			closest_dist = dist
	return closest


def calculateRoute(start,end,detour):#set up the problem and calculate the route

	start_id = getClosestNode(start)#get id of nearest actual node
	end_id = getClosestNode(end)#ditto

	if start_id == end_id: 
		#if they map to same cluster go direct
		results = {"score": 0, "cost": 0, "path":[start,end]}
		response = json.dumps(results)
		return response


	baseDistance = locations.gcdForLocations(start_id,end_id)

	maxDist = baseDistance + detour * maxDetour(baseDistance)

	init = time.clock()
	op = OrienteeringProblem(locations,start_id,end_id,maxDist)
	
	path = op.computePath(COMPUTE_TIME)
	costStr = "%.2f out of %.2f" % (path.get_cost(),maxDist)
	scoreStr = "%.2f" % path.get_total_score()
	
	print "Calcuated in %f seconds." % (time.clock() - init)
	
    #construct the path 
	pathCoords = []
	pathCoords.append(start)
	for node in path:#return a list of coordinates
		#ignore start and end as they as replaced with geocoded addr
		if node.location_id != start_id and node.location_id != end_id:
			pathCoords.append(node.coords)
	pathCoords.append(end)

	print pathCoords

	results = {"score" : scoreStr,"cost"  : costStr,"path"  : pathCoords}

	response  = json.dumps(results)
   	
	print response
	return response

#routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/_init',methods = ['GET'])
def init():
	result = json.dumps(locations.getLocations())
	return result

@app.route('/_getRoute',methods = ['GET'])
def getRoute():
	
	start_lat= request.args.get('start_lat',-1,type=float)
	start_lng = request.args.get('start_lng',-1,type=float)

	start = (start_lat,start_lng)

	print start 

	end_lat= request.args.get('end_lat',-1,type=float)
	end_lng = request.args.get('end_lng',-1,type=float)

	end = (end_lat,end_lng)

	print end
	
	detourFactor = request.args.get('detour',-1,type=float)#value between 0 and 1

	return calculateRoute(start,end,detourFactor)
	

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
