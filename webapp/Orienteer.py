"""
Orienteer.py: classes for computing a appromiate solution to the orienteering problem using genetic algorithm
Mark Lubin
"""

POPULATION_SIZE = 50
RADIUS = 6368 #radius of earth in kilometers

import Location,random
from math import acos,sin,cos,radians

class OrienteeringProblem:
  
  def __init__(self,locations,start,end,max_cost):#the problem itself
    self.locations = locations
    self.start = start
    self.end = end
    self.max_cost = max_cost
    self.vertices = locations.asIds()[:]
    self.vertices.remove(start)
    self.vertices.remove(end)
    self.queen = None
    
  def computePath(self,iterations):
    self.iterations = iterations
    self.population = self.seed_population(POPULATION_SIZE)
    cnt = 0
    while cnt < iterations: 
      cnt += 1
      self.population.sort(reverse = True)
      self.queen = self.population[0]
      self.cull()
      self.mutate()
    return self.queen
    
  def cull(self):pass
    
  def mutate(self):pass

      
    
  def seed_population(self,size):
    population = []
    while len(population) < size:
      population.append(self.construct_random_tour())
    return population
    
  def construct_random_tour(self):
    head = Node(self.start,0,0,0,self.locations.coordsForLocation(self.start))
    node = head
    random.shuffle(self.vertices)
    for lid in self.vertices:
      node.next = Node(lid,node,0,self.locations.importanceForLocation(lid),
      self.locations.coordsForLocation(lid))
      node = node.next
    node.next = Node(self.end,0,0,0,self.locations.coordsForLocation(self.end))
    return  self.make_feasible(Tour(head))
    
  def make_feasible(self,t):
    node = t.head.next
    while t.get_cost() > self.max_cost and node:
      toDelete = node
      node = node.next
      t.removeNode(toDelete.location_id)
    return t
      
      
class Tour:#a genetic "chromeosome", a path connecting start and end
  def __init__(self,head):
    self.head = head
    self.total_score = 0
    self.cost = 0
    
  def removeNode(self,location_id):
    node = self.head
    while node and node.location_id != location_id:
      node = node.next
    if not node: return
    node.next.prev = node.prev
    node.prev.next = node.next
    if self.cost: 
      self.cost -= self.greatCircleDistance(node.prev.coords,node.coords)
      self.cost -= self.greatCircleDistance(node.coords,node.next.coords)
      self.cost += self.greatCircleDistance(node.prev.coords,node.next.coords)
    if self.total_score: self.total_score -= node.score
    del node
    return 
  
  def get_cost(self):
    if not self.cost:
      node = self.head
      while node.next:
        self.cost += self.greatCircleDistance(node.coords,node.next.coords)
        node = node.next
    return self.cost

    
  def get_total_score(self):
    if not self.total_score:
      node = self.head
      while node:
        self.total_score += node.score
        node = node.next
    return self.total_score
    
    
  def greatCircleDistance(self,c1,c2):#great circle distance in km
    #TODO fix distance
    dLong = abs(c1[1] - c2[1]) #difference in longitude

    dAngle = acos(sin(c1[0]) * sin(c2[0])
                           + cos(c1[0]) * cos(c2[0]) * cos(dLong))

    #print self._locations.importanceForLocation(l2)
    d = RADIUS * dAngle
    #print "DISTANCE in KM: %f" % d
    return d
    
  def __cmp__(self,other):
    #import pdb; pdb.set_trace()
    if self.get_total_score() < other.get_total_score(): return -1
    elif self.get_total_score() == other.get_total_score(): return 0
    elif self.get_total_score() > other.get_total_score(): return 1
    
    
  def __str__(self):
    node = self.head
    string = ''
    while node:
      string += "%d-" % node.location_id
      node = node.next
    string += "\t COST: %f SCORE: %f" % (self.get_cost(),self.get_total_score())
    string += '\n'
    return string
    

class Node:#a node in the graph 
    def __init__(self,location_id,prev,next,score,coords):
      self.location_id = location_id
      self.prev = prev
      self.next = next
      self.score = score
      self.coords = coords
      
      
def main():
  l = Location.Locations()
  op = OrienteeringProblem(l,0,100,55000)
  print op.computePath(1)

  

if __name__ == '__main__':
  main()