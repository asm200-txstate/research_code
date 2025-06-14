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

from .GenIS import GenIS
from .MISIP import MISIP
from random import random
import time

import networkx as nx
from OutputPrint.Output import OutputPrint

class BYBBStrat:
    def __init__(self):
        self.GIS = GenIS()
        self.disp_info = OutputPrint()

        self.timer = 0                                                              # Pause the output terminal
    
    # def branch_scheme_helper(self, Graph : Graph, I : list, X : list, level : int): 
    def branch_scheme_helper(self, G : nx, I : list, X : list, lvl : int):

        S, U = self.GIS.gen_indset(G), []                                           # Generate an arbitrary independent set, S \subseteq V (Later Task: Use chordal method)
        V = list(G.nodes)

        valid = False                                                               # Step 1: Find a subset U \subseteq V such that \alpha(G[U]) <= |S|
        while not valid:
            U = [v for v in V if random() < 0.50]                                   # Randomly choose vertices - each v in V has a 50/50 probability 
            ISGraph = nx.induced_subgraph(G, U)                                     # Future task: Find a better way to choose U, randomness is too inefficient for a huge G

            MIS_model = MISIP(ISGraph)
            MIS_model.optimize()

            if MIS_model.opt_cost() <= len(S): valid = True                         # Display if candidate S staisfies a(G[U]) <= |S|

        # Newline output formatting for terminal - executed once 
        add_endl = True
        self.disp_info.print_top_line_break() if add_endl and lvl == 0 else None 
        add_endl = False if add_endl and lvl == 0 else add_endl

        if V == U: 
            MIS_model = MISIP(G)
            MIS_model.optimize()
            S = MIS_model.opt_soln()

            self.disp_info.print_final_lvl(lvl, S, I)
            return

        VnU = {v : G.degree(v) for v in V if v not in U}
        X_list = list(dict(sorted(VnU.items(), key = lambda item : item[1])).keys())    # Step 2: Sort vertices in V\U by degree of vertices 

        for i in range(len(VnU)):                                                       # Step 3: Construct Vi and apply recursive step 
            root = X_list[i]

            Xj_tilde, not_N = [], list(nx.non_neighbors(G, root))                       # Xj_tilde := {xj : j < i}
            for j in range(i): Xj_tilde.append(X_list[j])                               # Append vertices already seen into Xj_tilde

            Vi = not_N.copy()
            for v in Xj_tilde:                                                          # Perform set-minus operation to construct final Vi
                if v in not_N: Vi.remove(v)

            for v in V:                                                                 # Append current X and I candidates (Backtracking P-1)
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X.append(v)
            I.append(root)

            Gt = nx.induced_subgraph(G, Vi)                                             # Make an induces subgraph on Vis

            time.sleep(self.timer)

            lvl += 1                                                                  
            self.branch_scheme_helper(Gt, I, X, lvl)                                    # Call recursive case on ISG of G, I, X (Update level entry - Backtracking P-1.5)
            lvl -= 1

            for v in V:                                                                 # Remove current X and I candidates (Backtracking P-2)
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X.remove(v)
            I.remove(root)

            time.sleep(self.timer)                                                      # Pause terminal - meant to debug code / read terminal

        return

    def branch_scheme(self, G : nx):
        self.branch_scheme_helper(G, [], [], 0)
