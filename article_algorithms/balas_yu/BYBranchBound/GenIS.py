## ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** 
## Filename: main.py   
## 
## Author: Axel Sanchez Moreno
##
## Description: Text goes here ...
##
##
## Dependencies: 
##
## 
##
## 
##
##
##
##
## ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** 

from random import random
import Graph.Graph as Graph

class GenIS:
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name:  __init__ (Driver)
    # 
    # Description:  Initializes the instance of the graph G to the GenIS class. 
    #
    # Argument(s): 
    #   * V: Set of vertices to the graph G 
    #   * E: Set of edges to the graph G
    #
    # Return(s): None
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def __init__(self, G):
        self.Graph = G
    
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name:  gen_IS 
    # 
    # Description:  Generates an arbitrary independent set, S, to the graph self.G by randomly  
    #               choosing a vertex to be included and appends the vertex if that same vertex 
    #               is adjacent to another vertex that's adjacent to a vertex already in S.  
    # 
    # Argument(s): None 
    # 
    # Return(s): A generated independent set to the graph self.G 
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def gen_IS(self):
        S, V, E = [], self.Graph.get_allV(), self.Graph.get_allE()          ## S: The set of independent vertices to the graph G
        for v in V:
            invalid = False
            check_v = 1 if random() < 0.5 else 0                            ## Check: Is vertex v in V a candidate to add to S
            if check_v: 
                for s in S:                                                 ## Check: Is v adjacent to a vertex s already in S 
                    if [s, v] in E: 
                        invalid = True                                      ## If adjacent, move on to the next vertex in V
                        break
                if not invalid: S.append(v)                                 
        return S
