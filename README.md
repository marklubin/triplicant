TRIPLICANT - Travel discovery engine 
========================================

[demo](http://triplicant.heroku.com)

Overview
-----------
Triplicant attempts to recommend an optimal travel route given a start and end point and a "detour factor", which represents how much time/money/etc. you are willing to spend travelling between the ends points. It identifies popular locations and ranks them using photo metadata extracted from the Flickr API. Then it uses a genetic algorithm to approximate a solution to the "Orienteering" problem.
 
Technology
--------------
This project is built primarily in Python using the Flask microframework for the web backend. I've used Postgres for the data store and jQuery for the fancy front end with the help of Google Maps API to make sense of it all.


Behind the scenes
--------------------
Triplicant uses some interesting concepts from AI, such as:

### Clustering

Uses a mean-shift clustering algorithm to identify about 600 clusters(locations) each with about a radius of 4 miles where many photos have been taken.

### Graph centrality

The notion of centrality of a graph is a measure of a vertex's overall importance within the graph. Here I used probability of transit between two locations, after reducing a users photo history to an ordered sequence of locations they visited, combined with the total number of photos taken in a location to compute the centrality of each node in a way that is similar to the method of eigenvector centrality, in particularly the algorithm is highly influenced by Google PageRank. The set of equations for the importance of each vertex is then solved using a value iteration method.

### Solving the orienteering problem via a GA

At first I had intend to use my importance values in a simple model of path cost and compute a A* graph search. However, quickly found that I was modeling problem incorrectly. After some research I found that the problem I was actually trying to solve is the point-to-point orienteering problem. My version of this problem is: 

Given:
* G = (V,E) is a fully connected undirected graph
* let each vertex have a "score" associated with it (importance in this case) eg. s: V -> R
* let each edge have a path cost, in this problem I've simply used the great circle distance between the locations. d : E -> R
* a hard upper limit on the acceptable path cost 
* a start node and an end node

Find:
* the path from the start node to the end node that has the highest possible score of the paths with acceptable path costs, where the score of a path is the sum score of the nodes it visits

Or rather, find a path that connects the start and end and visits the most interesting destinations in-between given a travel budget.

Unfortunately, as this problem is reducible to a variant of the Travelling Salesman Problem it is also NP-hard and the exact solution can't be computed for a worthwhile number of nodes in a reasonable time. Thus, I've used a "queen-bee" genetic algorithm to approximate a solution.  The algorithm can be described as follows:

1. Generate a population of random paths between the start and end using all the other nodes
2. remove nodes from random points along the paths until the path cost is acceptable
3. rank the population by fitness, the fittest member of the population becomes "the queen", the top half of the rest have a chance to crossover with the queen
4. for each remaining paths, with a certain probability generate a new path by probabilistically building it out the queen's and the path's components
5. for each new path, "mutate" with a certain probability, that is to say insert a node taken from a probability distribution where the nodes are weighed by score and insert it at a random point along the path.
6. remove nodes from random points until the path cost of the new path is acceptable
7. permute each path to see if a different ordering would have a lower path cost
8. repeat 3-7 for a given number of iterations(generations) and return the queen of the last generation

Innovation
---------------

Triplicant builds on some existing research in various fields of AI and combines them in a novel way. As far as I know Triplicant is the first app of its kind to:

* apply clustering to identify locations from photo metadata on a global scale
* attempt to weight travel destinations by computing their centrality within a graph
* apply a GA to this instance of the orienteering problem
* combine the above ideas to try to produce travel routes

