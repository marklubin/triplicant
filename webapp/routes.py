"""
routes.py
main entry point for web application
Mark Lubin
"""
DEBUG = True
COMPUTE_TIME = 200

from flask import Flask,url_for,render_template,request
from Location import Locations
from Orienteer import OrienteeringProblem,Tour,Node
import json

app = Flask(__name__)#Flask app object
locations = Locations()

def calculateRoute(start_id,end_id,detour):#set up the problem and calculate the route
	baseDistance = locations.gcdForLocations(start_id,end_id)
	maxDist = baseDistance * detour 
	op = OrienteeringProblem(locations,start_id,end_id,maxDist)
	path = op.computePath(COMPUTE_TIME)
	pathCoords = []
	for node in path:#return a list of coordinates
		pathCoords.append(node.coords)

   	results = json.dumps(pathCoords)
   	print results
   	return results

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
	detourFactor = request.args.get('detour',-1,type=float)

	return calculateRoute(start_id,end_id,detourFactor)
	

if __name__ == '__main__':
    app.run(debug = DEBUG)#start server
