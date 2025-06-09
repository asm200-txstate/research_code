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

from OutputPrint.Output import OutputPrint

class BYBBStrat:
    def __init__(self, G : Graph):
        self.Graph = G
        V, E = self.Graph.get_all_v(), self.Graph.get_all_e()
        self.GIS = GenIS()
        self.GenISG = GenISGraph()
        self.disp_info = OutputPrint()

        self.label_width = 32
        self.timer = 0
    
    def branch_scheme_helper(self, Graph : Graph, I : list, X : list, level : int): 
        S, U = self.GIS.gen_indset(Graph), []                                           # Generate an arbitrary independent set, S \subseteq V
        V = Graph.get_all_v()

        valid = False                                                                   # Step 1: Find a subset U \subseteq V such that \alpha(G[U]) <= |S|
        while not valid:
            U = [v for v in V if random() < 0.50]                                       # Randomly choose vertices - each v in V has a 50/50 probability 
            ISGraph = self.GenISG.gen_isgraph(Graph, U)                                 # Future task: Find a better way to choose U, randomness is too inefficient for a huge G

            MIS_model = MISIP(ISGraph)
            MIS_model.optimize()

            # Display if candidate S staisfies a(G[U]) <= |S|
            if MIS_model.opt_cost() <= len(S): valid = True                                                          

        # Newline output formatting for terminal - executed once 
        add_endl = True
        self.disp_info.print_top_line_break() if add_endl and level == 0 else None 
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

        for i in range(len(VnU)):                                                       # Step 3: Construct Vi and apply recursive step 
            root = X_list[i]

            Xj_tilde, not_N = [], Graph.non_neighborhood(root)                          # Xj_tilde := {xj : j < i}
            for j in range(i): Xj_tilde.append(X_list[j])                               # Append vertices already seen to Xj_tilde

            Vi = not_N.copy()
            for v in Xj_tilde:                                                          # Perform set-minus operation to construct final Vi
                if v in not_N: Vi.remove(v)

            for v in V:                                                                 # Append current X and I candidates (Backtracking P-1)
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X.append(v)
            I.append(root)

            self.disp_info.print_rec_level(level)                                       # Printing current data at a certain node in the tree algorithm

            self.disp_info.print_p1(V, S, U)
            self.disp_info.print_p2(root, X_list, not_N)

            self.disp_info.print_p3(i, Xj_tilde, Vi)
            self.disp_info.print_p4(I, X)

            self.disp_info.print_line_break()

            Graph_t = self.GenISG.gen_isgraph(Graph, Vi)                                # Make an induces subgraph on Vi

            time.sleep(self.timer)                                                      # ** Pause terminal ** - meant to debug code / read terminal

            level += 1                                                                  
            self.branch_scheme_helper(Graph_t, I, X, level)                             # Call recursive case on ISG of G, I, X (Update level entry - Backtracking P-1.5)
            level -= 1

            for v in V:                                                                 # Remove current X and I candidates (Backtracking P-2)
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X.remove(v)
            I.remove(root)

            time.sleep(self.timer)                                                      # ** Pause terminal ** - meant to debug code / read terminal

    def branch_scheme(self):
        self.branch_scheme_helper(self.Graph, [], [], 0)
