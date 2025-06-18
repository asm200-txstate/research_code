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
from itertools import combinations

class GenGraph:
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: __init__ (Driver)
    #
    # Description: Constructor to the GenGraph class.
    #
    # Argument(s):
    #    * card_V: The number of vertices to the graph G
    #
    # Return(s): None
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def __init__(self, card_V=-1):
        if card_V <= -1:
            print("Invalid |V|, setting |V| = 10")
            card_V = 10
        self.card_V = card_V
    
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: gen_V
    #
    # Description: Generates the set of vertices, V, to the graph G.
    #
    # Argument(s): None
    #
    # Return(s): None
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def gen_V(self):
        V = []
        for v in range(self.card_V): V.append(v+1)
        return V
    
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: gen_E
    #
    # Description: Generates the set of edges, E, to the graph G.
    #
    # Argument(s): None
    #
    # Return(s): None
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def gen_E(self):
        E = []
        for edge in combinations(range(self.card_V), 2):
            edge = [v + 1 for v in edge]
            if random() < 0.50: E.append(edge)
        return E
