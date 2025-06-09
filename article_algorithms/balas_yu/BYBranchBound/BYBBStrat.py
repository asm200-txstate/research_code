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

        self.label_width = 28
        self.timer = 0
    
    def find_mis_helper(self, Graph : Graph, I : list, X : list, level : int): 
        S, U = self.GIS.gen_indset(Graph), []                                           # Generate an arbitrary independent set, S \subseteq V
        V = Graph.get_all_v()

        valid = False                                                                   # Step 1: Find a subset U \subseteq V such that \alpha(G[U]) <= |S|
        while not valid:
            U = [v for v in V if random() < 0.50]      
            ISGraph = self.GenISG.gen_isgraph(Graph, U)

            MIS_model = MISIP(ISGraph)    
            MIS_model.optimize()

            # Display if candidate S staisfies a(G[U]) <= |S|
            if MIS_model.opt_cost() <= len(S): valid = True                                                          

        # Newline output formatting for terminal - executed once 
        add_endl = True
        print("\n" + "*" * 75, "\n") if add_endl and level == 0 else None 
        add_endl = False if add_endl and level == 0 else add_endl

        VnU = {v : Graph.degree(v)-1 for v in V if v not in U}

        if V == U: 
            MIS_model = MISIP(Graph)
            MIS_model.optimize()
            S = MIS_model.opt_soln()
            
            print(f">>> {f'Final Solution (level = {level}): ':<{self.label_width}} {S + I}")
            print(f">>> {f'Independent set S: ':<{self.label_width}} {S}")
            print(f">>> {f'Independent set I: ':<{self.label_width}} {I}")
            print("\n" + "*" * 75 + "\n")

            return

        # Sort the entries based on the degree
        X_list = list(dict(sorted(VnU.items(), key = lambda item : item[1])).keys())    # Step 2: Sort vertices in V\U by degree of vertices 
        # print(f">>> {'Current VnU (By Degree):':<{self.label_width}} {X_list}\n")

        for i in range(len(VnU)):                                                        # Step 3: Construct Vi and apply recursive step 
            root = X_list[i]

            Xi_tilde, not_N = [], Graph.non_neighborhood(root)
            for j in range(i): Xi_tilde.append(X_list[j])

            Vi = not_N.copy()
            for v in Xi_tilde: 
                if v in not_N: Vi.remove(v)

            # Append current X and I candidates
            for v in V:
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X.append(v)
            I.append(root)

            print(f">>> {f'Current Recursion Level:':<{self.label_width}} Level {level}")
            print(f">>> {f'Current vertex set - V:':<{self.label_width}} {V}")
            print(f">>> {f'Current Independent set S:':<{self.label_width}} {S}\n")

            print(f">>> {'Candidate set - U:':<{self.label_width}} {U}")
            print(f">>> {'Current VnU (By Degree):':<{self.label_width}} {X_list}\n")

            print(f">>> {f'Current Node in VnU:':<{self.label_width}} Node {root}")
            print(f">>> {f'Current not_N({root})':<{self.label_width}} {not_N}")
            print(f">>> {f'Current X{i}_tilde:':<{self.label_width}} {Xi_tilde}")
            print(f">>> {f'Current V{i} | New V:':<{self.label_width}} {Vi}\n")

            print(f">>> {'Included Set (I):':<{self.label_width}} {I}")
            print(f">>> {'Excluded Set (X):':<{self.label_width}} {X}\n")

            print("*" * 75, "\n")

            # Make an induces subgraph on Vi
            Graph_t = self.GenISG.gen_isgraph(Graph, Vi)

            # Pause terminal - meant to debug code / read terminal
            time.sleep(self.timer)

            # Call recursive case on ISG of G, I, X
            level += 1
            self.find_mis_helper(Graph_t, I, X, level)
            level -= 1

            # Remove current X and I candidates
            for v in V:
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X.remove(v)
            I.remove(root)

            # Pause terminal - meant to debug code / read terminal
            time.sleep(self.timer)

    def find_mis(self):
        self.find_mis_helper(self.Graph, [], [], 0)
