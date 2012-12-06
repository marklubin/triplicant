"""
Orienteer.py: classes for computing a appromiate solution to the orienteering problem using genetic algorithm
Mark Lubin
"""


RADIUS = 6368 #radius of earth in kilometers

import Location,random,time,walkerRandom
from math import acos,sin,cos,radians,ceil


class OrienteeringProblem:
  
  def __init__(self,locations,start,end,max_cost):#the problem itself
    self.POPULATION_SIZE = 40
    self.CROSSOVER_PROB = .95
    self.MUTATION_PROB = .95
    self.CLOSEST_NODE_PROB = .5
    
    
    self.locations = locations
    self.start = start
    self.end = end
    self.max_cost = max_cost
    self.vertices = locations.asIds()[:]
    self.vertices.remove(start)
    self.vertices.remove(end)
    self.queen = None
    
    probablities = {}

    for vertex in self.vertices:#create a weighted probablity distrobution for mutations
      probablities[vertex] = self.locations.importanceForLocation(vertex)

    self.distribution = walkerRandom.Walkerrandom(probablities.values(),probablities.keys())
    
  def computePath(self,iterations):
    self.iterations = iterations
    self.population = self.seed_population(self.POPULATION_SIZE)
    cnt = 0
    if not iterations:#for comparision, do nothing but return the best random
      self.population.sort(reverse = True)
      return self.population[0]
    while cnt < iterations: 
      #print cnt
      cnt += 1
      self.population.sort(reverse = True)#get the top one
      self.queen = self.population[0]
      self.queen.shuffle()
      mates = self.cull()#only keep the top half
      self.population = self.nextGeneration(mates)#generate the next gen
    self.queen.shuffle()
    return self.queen
    
  def cull(self):
    return self.population[1:int(ceil(self.POPULATION_SIZE/2))]
    
  def nextGeneration(self,mates):#probablitistically mate with queen
    #print "Creating next generation"
    newPop = []
    newPop.append(self.queen)#always keep the queen
    queens_genes = self.getGenes(self.queen)
    for mate in mates:
      if random.random() < self.CROSSOVER_PROB:#TODO make more fit mates have better chance
        newPop += self.spawn(queens_genes,self.getGenes(mate))#returns two spawns
      else:
        mate.shuffle()#shuffle this guy
        newPop.append(mate) #otherwise this guy makes it to the next gen
    return newPop
        
  def spawn(self,A,B):
    # print "Spawning"
    spawn = []
    i = 0


    while i in range (0,2):#doing this twice
      spawn.append(Tour())
      start = Node(self.start,0,self.locations.coordsForLocation(self.start))
      spawn[i].append(start)
      current = start
      visited = [start.location_id]

      #construct the spawn
      while current.location_id != self.end:#beak 
        canidates = []#the crossover matrix
        if current.location_id in A.keys():#all possibles from A
          canidates += A[current.location_id]
        if current.location_id in B.keys():#from B
          canidates += B[current.location_id]
        possibles = [c for c in canidates if c.location_id not in visited]#we don't allow duplicate visits
        if not possibles: #this is a bad canidate, has a cycle, so dismiss it
          spawn[i] = []
          break
        next = current.findClosest(possibles)#find the closet amongst possibles
        if random.random() < self.CLOSEST_NODE_PROB:#sometimes choose randomly
          next = random.choice(possibles)  
        spawn[i].append(next)
        visited.append(next.location_id)
        current = next

      if not spawn[i]:#if this was a dud canidate continue
        i = i +1
        break 

      #sometimes inject a random node into the spawn  
      if random.random() < self.MUTATION_PROB:#with some probablity insert a random node in the path at a random pos
        allowed = [lid for lid in self.locations.asIds() \
                    if lid not in [n.location_id for n in spawn[i].nodes]]
        mutant = None #get a mutant from the weighted distobution

        while True:
          mutant = self.distribution.random()
          if mutant in allowed: break

        index = random.choice(range(1,len(spawn[i].nodes)))
        mNode = Node(mutant,self.locations.importanceForLocation(mutant),
        self.locations.coordsForLocation(mutant))
        spawn[i].insert(index,mNode)
      
      spawn[i].shuffle()#shuffle the newly made tour
      self.make_feasible(spawn[i])
      i += 1

    return [s for s in spawn if s]#return valid spawns
      
  def getGenes(self,tour):#return the genes for a tour
    #each row has the adjacent nodes in the tour to node i 
    genes = {}
    start = tour.nodes[0]
    end = tour.nodes[len(tour.nodes) -1]
    genes[start.location_id] = [tour.next(start.location_id)]
    genes[end.location_id] = [tour.prev(end.location_id)]
    for node in tour.nodes[1:len(tour.nodes)-1]:
      genes[node.location_id] = [tour.prev(node.location_id),tour.next(node.location_id)]
    return genes
  
    
  def seed_population(self,size):#construct the seed population
    population = []
    while len(population) < size:
      population.append(self.construct_random_tour())
    return population
    
  def construct_random_tour(self):
    Node(self.start,0,self.locations.coordsForLocation(self.start))
    t = Tour()
    t.append(Node(self.start,0,self.locations.coordsForLocation(self.start)))
    possibles = random.sample(self.vertices,len(self.vertices)/2)#for performance only look at half at a time
    for lid in possibles:
      t.append(Node(lid,self.locations.importanceForLocation(lid),
      self.locations.coordsForLocation(lid)))
    t.append(Node(self.end,0,self.locations.coordsForLocation(self.end)))
    self.make_feasible(t)
    return t
    
  def make_feasible(self,t):#remove a random node until the tour has an acceptable cost
    nodes = t.getRemoveable()
    while t.get_cost() > self.max_cost and nodes:
      toDelete = random.choice(nodes)
      nodes.remove(toDelete)
      t.removeNodeWithLocationId(toDelete)
      
class Tour:#a genetic "chromosome", a path connecting start and end
  def __init__(self):
    self.SHUFFLE_TIMES = 10
    self.nodes = []
    self.total_score = 0
    self.cost = 0
    
  def append(self,node):
    self.nodes.append(node)
    self.cost = 0
    
  def insert(self,index,node):
    self.nodes.insert(index,node)
    self.cost = 0
    self.get_cost()
    self.total_score += node.score
    
  def next(self,location_id):
    node_index = self.indexForLocationId(location_id)
    return self.nodes[node_index + 1]
    
  def prev(self,location_id):
    node_index = self.indexForLocationId(location_id)
    return self.nodes[node_index - 1]
  
  def getRemoveable(self):#everything but start and end
    return [node.location_id for node in self.nodes[1:len(self.nodes)-1]]
    
  def indexForLocationId(self,location_id):
    for n in self.nodes:
      if n.location_id == location_id: return self.nodes.index(n)
      
    
  def removeNodeWithLocationId(self,location_id):
    i= self.indexForLocationId(location_id)
    if self.cost: 
      self.cost -= self.greatCircleDistance(self.nodes[i].coords,self.nodes[i+1].coords)
      self.cost -= self.greatCircleDistance(self.nodes[i-1].coords,self.nodes[i].coords)
      self.cost += self.greatCircleDistance(self.nodes[i-1].coords,self.nodes[i+1].coords)
    if self.total_score: self.total_score -= self.nodes[i].score
    self.nodes.remove(self.nodes[i])
    return
  
  def get_cost(self):
    if not self.cost:
     i = 0
     while i+1 in range(0,len(self.nodes)):
       self.cost += self.greatCircleDistance(self.nodes[i].coords,self.nodes[i+1].coords)
       i += 1
    return self.cost
    
  def get_total_score(self):
    if not self.total_score:
      self.total_score = sum([node.score for node in self.nodes])
    return self.total_score


  def shuffle(self):#try nodes in a different order to see if cost is lower
    lowCost = self.get_cost()
    shuffleable = self.nodes[1:len(self.nodes) -1]
    
    cnt = 0
    while cnt < self.SHUFFLE_TIMES:
      last = self.nodes[:]
      random.shuffle(shuffleable)
      self.nodes = [last[0]] + shuffleable + \
                    [last[-1]]
      self.cost = 0
      cnt += 1
      if self.get_cost() < lowCost:
        lowCost = self.get_cost()
        continue
      else:
        self.nodes = last
        self.cost = 0
        continue
    
    return
    
  def greatCircleDistance(self,c1,c2):#great circle distance in km
    c1 = [radians(c) for c in c1]
    c2 = [radians(c) for c in c2]
    dLong = abs(c1[1] - c2[1]) #difference in longitude

    dAngle = acos(sin(c1[0]) * sin(c2[0])
                           + cos(c1[0]) * cos(c2[0]) * cos(dLong))

    #print self._locations.importanceForLocation(l2)
    d = RADIUS * dAngle
    #print "DISTANCE in KM: %f" % d

    return d
    
  def __setitem__(self,index,value):
    self.nodes[index] = value
    
  def __getitem__(self,index):
    return self.nodes[index]
    
  def __cmp__(self,other):#make sortable
    if self.get_total_score() < other.get_total_score(): return -1
    elif self.get_total_score() == other.get_total_score(): return 0
    elif self.get_total_score() > other.get_total_score(): return 1
    
    
  def __str__(self):
    string = ''
    string += str([node.location_id for node in self.nodes])
    string += "\t COST: %f SCORE: %f" % (self.get_cost(),self.get_total_score())
    string += '\n'
    return string
    

class Node:#a node in the graph 
    def __init__(self,location_id,score,coords):
      self.location_id = location_id
      self.score = score
      self.coords = coords
      
    def findClosest(self,nodes):
      distance = 99999
      best = None
      for node in nodes:
        gcd = greatCircleDistance(self.coords,node.coords)
        if gcd < distance:
          distance = gcd
          best = node
      return best
        
    
      

def greatCircleDistance(c1,c2):#great circle distance in km
  c1 = [radians(c) for c in c1]
  c2 = [radians(c) for c in c2]
  dLong = abs(c1[1] - c2[1]) #difference in longitude

  dAngle = acos(sin(c1[0]) * sin(c2[0])
                      + cos(c1[0]) * cos(c2[0]) * cos(dLong))

  d = RADIUS * dAngle
  return d


def main():
  l = Location.Locations()
  start = time.clock()
  op = OrienteeringProblem(l,1,26,1600)
  tour = op.computePath(150)
  print tour
  for lid in [node.location_id for node in tour.nodes]: print l.placenameForLocation(lid)
  print "Calcuated in %f seconds." % (time.clock() - start)

  

if __name__ == '__main__':
  main()