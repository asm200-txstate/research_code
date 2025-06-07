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

import Graph.Graph as Graph
from .GenIS import GenIS
from .MISIP import MISIP
from Graph.GenISG import GenISGraph
from random import random
import time

from Graph.GraphPlot import GraphPlot

class BYBBStrat:
    def __init__(self, G : Graph):
        self.Graph = G
        V, E = self.Graph.get_all_v(), self.Graph.get_all_e()
        self.GIS = GenIS()
        self.GenISG = GenISGraph()
    
    def find_mis_helper(self, Graph : Graph, I : list, X : list): 
        S, U = self.GIS.gen_indset(Graph), []                                           # Generate an arbitrary independent set, S \subseteq V
        V = self.Graph.get_all_v()

        print(f">>> Current set V: {V}")
        print(f">>> Independent set S: {S}")
        print(f">>> Size (|S|): {float(len(S))}")
        print("")

        valid = False                                                                   # Find a subset U \subseteq V such that \alpha(G[U]) <= |S|
        while not valid:
            U = [v for v in self.Graph.get_all_v() if random() < 0.50]
            ISGraph = self.GenISG.gen_isgraph(Graph, U)

            MIS_model = MISIP(ISGraph)    
            MIS_model.optimize()
            cost = MIS_model.opt_cost()

            print("")
            print(">>> Candidate set U:", U)
            print(">>> Cost (a(G[U])):", cost)

            if MIS_model.opt_cost() <= len(S): 
                print(">>> a(G[U]) <= |S|")
                print("")
                valid = True
            else: 
                print(">>> a(G[U]) > |S| ...")

            time.sleep(2.5)                                                             # Pause terminal every 2.5 second, meant for debugging code / reading terminal. 

        # Arrange vertices in V\U by the degree in G
        VnU = {}

        for v in V: 
            if v not in U: 
                deg = Graph.degree(v)
                VnU[v] = deg
        
        x = dict(sorted(VnU.items(), key = lambda item : item[1]))                      # Sort vertices in V\U by the degree at each vertex (ascending order)

        print(">>> V\\U:", list(VnU.keys()))
        print(">>> x key:", list(x.keys()))
        print(">>> x deg:", list(x.values()))
        print("")

        for v in VnU: print(f"not_N({v}): {Graph.non_neighborhood(v)}")

        # Display the induced subgraph, ISGraph, within the full graph, G (after ~ 15 seconds)
        GPlot = GraphPlot(self.Graph)
        for v in VnU:
            ISG = self.GenISG.gen_isgraph(Graph, Graph.non_neighborhood(v))
            GPlot.disp_isgraph(ISG)

    def find_mis(self):
        self.find_mis_helper(self.Graph, [], [])

        # S, U = self.GIS.gen_indset(self.Graph), []
        # print("Generated independent set S:", S)

        # MIS_model = MISIP(self.Graph)
        # MIS_model.optimize(S)
        
        # # To be implemented later ...
        # print("Optimal Cost:", MIS_model.opt_cost())
        # print("Optimal Soln:", MIS_model.opt_soln())