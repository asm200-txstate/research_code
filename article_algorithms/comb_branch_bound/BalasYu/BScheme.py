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

import time
import networkx as nx
from random import random
from random import randint

from OutputPrint.Output import OutputPrint

from .RecSimpFix import RSF
from .MISIP import MISIP
from .CCIP import CCIP
from .GreedyMethod import GMethod
from .ChordalMethod import ChordalMethod

from BalasXue.WChordalMethod import WCMethod

class BYBScheme:
    def __init__(self):
        self.disp_info = OutputPrint()
        self.timer = 0                                                              # Pause the output terminal
    
    # def branch_scheme_helper(self, Graph : Graph, I : list, X : list, level : int): 
    def branch_scheme_helper(self, G : nx, I : list, X : list, lvl : int, W : dict):
        print(f"Current level: {lvl}")

        # MGreedy = GMethod(G)
        # MGreedy.greedy_cc()
        # U, S = MGreedy.gen_sets()

        MChordal = ChordalMethod(G)
        MChordal.chordal_method()
        U, S = MChordal.gen_sets()

        # Note to reader: Wouldn't make sense since you're looking at the weights themselves and not the vertices in the set. 
        # MWChordal = WCMethod(G, W)
        # MWChordal.wc_method()
        # U, S = MWChordal.gen_sets()

        V = list(G.nodes)

        mis_model = MISIP(nx.induced_subgraph(G, U))
        mis_model.optimize()

        cc_model = CCIP(G, list(nx.find_cliques(G)))
        cc_model.optimize()

        print(f"\n|S| = {len(S)}")
        print(f"a(G[U]) = {mis_model.opt_cost()}")
        print(f"p(G[U]) = {cc_model.opt_cost()}\n")

        # print(f"len(S) = {len(S)} | a(U) = {mis_model.opt_cost()}")

        VnU = {v : G.degree(v) for v in V if v not in U}
        X_list = list(dict(sorted(VnU.items(), key = lambda item : item[1])).keys())   # Step 2: Sort vertices in V\U by degree of vertices 

        for i in range(len(VnU)):                                                      # Step 3: Construct Vi and apply recursive step 
            root = X_list[i]

            # print(f"Here at {root}")

            Xj_tilde, not_N = [], list(nx.non_neighbors(G, root))                      # Xj_tilde := {xj : j < i}
            for j in range(i): Xj_tilde.append(X_list[j])                              # Append vertices already seen into Xj_tilde

            Vi = not_N.copy()
            for v in Xj_tilde:                                                         # Perform set-minus operation to construct final Vi
                if v in not_N: Vi.remove(v)

            for v in V:                                                                # Append current X and I candidates (Backtracking P-1)
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X.append(v)
            I.append(root)

            Gt = nx.induced_subgraph(G, Vi)                                            # Make an induces subgraph on Vis

            time.sleep(self.timer)

            lvl += 1                                                                  
            self.branch_scheme_helper(Gt, I, X, lvl, W)                                   # Call recursive case on ISG of G, I, X (Update level entry - Backtracking P-1.5)
            lvl -= 1

            for v in V:                                                                # Remove current X and I candidates (Backtracking P-2)
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X.remove(v)
            I.remove(root)

            time.sleep(self.timer)                                                     # Pause terminal - meant to debug code / read terminal

        return

    def branch_scheme(self, G : nx):
        W = {}
        for v in G.nodes: W[v] = randint(0, 10)
        self.branch_scheme_helper(G, [], [], 0, W)
