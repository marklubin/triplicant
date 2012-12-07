"""
routes.py
main entry point for web application
Mark Lubin
"""
DEBUG = False
COMPUTE_TIME = 200

from flask import Flask,url_for,render_template,request
from Location import Locations
from Orienteer import OrienteeringProblem,Tour,Node
import json,time,os
from math import sqrt

maxDetour = lambda x: 40.0/sqrt(x) * x ;#special non-linear function for detour calculation
app = Flask(__name__)#Flask app object
locations = Locations()

def calculateRoute(start_id,end_id,detour):#set up the problem and calculate the route
	baseDistance = locations.gcdForLocations(start_id,end_id)

	maxDist = baseDistance + detour * maxDetour(baseDistance)
	print baseDistance, maxDist
	start = time.clock()
	op = OrienteeringProblem(locations,start_id,end_id,maxDist)
	path = op.computePath(COMPUTE_TIME)
	costStr = "%.2f out of %.2f" % (path.get_cost(),maxDist)
	scoreStr = "%.2f" % path.get_total_score()
	print "Calcuated in %f seconds." % (time.clock() - start)
	pathCoords = []
	for node in path:#return a list of coordinates
		pathCoords.append(node.coords)

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
	start_id = request.args.get('start_id',-1,type=int)
	end_id = request.args.get('end_id',-1,type=int)
	detourFactor = request.args.get('detour',-1,type=float)#value between 0 and 1

	return calculateRoute(start_id,end_id,detourFactor)
	

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
