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
    
    def find_mis_helper(self, Graph : Graph, I : list, X : list, level : int): 
        S, U = self.GIS.gen_indset(Graph), []                                           # Generate an arbitrary independent set, S \subseteq V
        V = Graph.get_all_v()

        # print(f">>> Current set V: {V}")
        # print(f">>> Independent set S: {S}")
        # print(f">>> Size (|S|): {float(len(S))}\n")

        valid = False                                                                   # Step 1: Find a subset U \subseteq V such that \alpha(G[U]) <= |S|
        while not valid:
            U = [v for v in V if random() < 0.50]      
            ISGraph = self.GenISG.gen_isgraph(Graph, U)

            MIS_model = MISIP(ISGraph)    
            MIS_model.optimize()
            cost = MIS_model.opt_cost()

            # print("\n>>> Cost (a(G[U])):", cost)
            if MIS_model.opt_cost() <= len(S): valid = True

            # if valid: print(">>> a(G[U]) <= |S|\n")
            # else: print(">>> a(G[U]) > |S| ...")

            # time.sleep(1.5)                                                             # Pause terminal every 1.5 second, meant for debugging code / reading terminal. 

        # print(f">>> U: {U}\n")

        VnU = {v : Graph.degree(v) for v in V if v not in U}

        if V == U: 
            MIS_model = MISIP(Graph)
            MIS_model.optimize()
            S = MIS_model.opt_soln()
            print(f">>> Final Solution: {S + I} at level {level}\n")

            ISGraph = self.GenISG.gen_isgraph(Graph, S + I)
            
            GPlot = GraphPlot(self.Graph)
            GPlot.disp_isgraph(ISGraph)

            return

        X_list = list(dict(sorted(VnU.items(), key = lambda item : item[1])).keys())

        # print(f">>> V\\U keys: {list(VnU.keys())}")
        # print(f">>> V\\U vals: {list(VnU.values())}\n")
        # print(f">>> X: {X_list}\n")

        # for v in VnU: print(f"not_N({v}): {Graph.non_neighborhood(v)}\n")

        for i in range(len(VnU)): 
            root = X_list[i]

            Xi_tilde, not_N = [], Graph.non_neighborhood(root)
            for j in range(i): Xi_tilde.append(X_list[j])

            Vi = not_N.copy()
            for v in Xi_tilde: 
                if v in not_N: Vi.remove(v)

            # print(f"Old V: {V}")
            # print(f"Current not_N({root}): {not_N}")
            # print(f"Current X{i}_tilde: {Xi_tilde}")
            # print(f"Current V{i} / New V: {Vi}")

            for v in V:
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X.append(v)
            I.append(root)

            # # Apply backtracking to X and I
            # print(f"Current I: {I}")
            # print(f"Current X: {X}\n")

            # Make an induces subgraph on Vi
            Graph_t = self.GenISG.gen_isgraph(Graph, Vi)
            print(f"Vertices: {Graph_t.get_all_v()} - Level: {level}")
            print(f"Edges: {Graph_t.get_all_e()} - Level: {level}\n")

            # Call recursive case on ISG of G, I, X
            level += 1
            self.find_mis_helper(Graph_t, I, X, level)
            level -= 1

            for v in V:
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X.remove(v)
            I.remove(root)

            # time.sleep(1.5)                                                             # Pause terminal every 1.5 second, meant for debugging code / reading terminal. 

    def find_mis(self):
        self.find_mis_helper(self.Graph, [], [], 0)
