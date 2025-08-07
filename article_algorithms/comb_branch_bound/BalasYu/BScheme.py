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
        self.VnU_index = -1
        self.VnU_S_set = []

        self.base_mis = []
        self.curr_mis_collection = {}
    
    def branch_scheme_helper(self, G : nx, I : list, X : list, lvl : int, W : dict):

        # Step 1: Given a graph G and an independnet set S, find a subset of S, called U, where alpha(G[U]) <= |S|

        MChordal = ChordalMethod(G)                                                 # Applying Chordal Method to G                
        MChordal.execute_cm()
        U, S = MChordal.gen_sets()   

        V = list(G.nodes)                                                   # Collect the whole set of vertices in G.

        # # MGreedy = GMethod(G)
        # # MGreedy.greedy_cc()
        # # U, S = MGreedy.gen_sets()

        # # Note to reader: Wouldn't make sense since you're looking at the weights themselves and not the vertices in the set. 
        # # MWChordal = WCMethod(G, W)
        # # MWChordal.wc_method()
        # # U, S = MWChordal.gen_sets()

        # print(f"U set : {U}")
        # print(f"S set : {S}")

        mis_model = MISIP(nx.induced_subgraph(G, U))
        mis_model.optimize()

        cc_model = CCIP(G, list(nx.find_cliques(G))) # Need to apply it to a susbet of cliques. 
        cc_model.optimize()

        # VnU = {v : G.degree(v) for v in V if v not in U}
        # X_list = list(dict(sorted(VnU.items(), key = lambda item : item[1])).keys())   # Step 2: Sort vertices in V\U by degree of vertices 

        # # print(f"\nmis(G[U]) = {mis_model.opt_cost()}")
        # # print(f"mcc(G[U]) = {cc_model.opt_cost()}\n")
        # # print(f"VnU List: {X_list}\n")

        # # print(f"V list: {V}")
        # # print(f"U list: {U}")

        # if X_list == []:
        #     print("\n*****")
        #     print(f"Hit the VnU emptyset! - Root Index: {self.VnU_index}")
        #     print(f"Final S set: {self.VnU_S_set}")
        #     print("*****")
        #     print(f"X List: {X}")
        #     print(f"I List: {I}")
        #     print("*****\n")

        #     if self.VnU_index != -1: 
        #         temp_set = self.VnU_S_set.copy()
        #         temp_set.append(self.VnU_index)
        #         if self.VnU_index not in self.curr_mis_collection:                        # Index has not been seen set 
        #             self.curr_mis_collection[self.VnU_index] = temp_set       
        #         elif len(self.curr_mis_collection[self.VnU_index]) > len(temp_set):       # Index has been seen in set, check if the
        #             self.curr_mis_collection[self.VnU_index] = temp_set                   # candidate set better/larger than the current set.
                
        # if lvl == 0:  
        #     print(f"\nLevel 0: ")
        #     print(f"VnU List: {X_list}")
        #     print(f"Set S: {S}")
        #     self.base_mis = S

        # elif lvl == 1: print(f"\nLevel 1 Set S: {S}")

        # for i in range(len(VnU)):                                                      # Step 3: Construct Vi and apply recursive step 
        #     root = X_list[i]

        #     # print(f"Here at {root}")

        #     if lvl == 0: self.VnU_index = root
        #     elif lvl == 1: self.VnU_S_set = S

        #     Xj_tilde, not_N = [], list(nx.non_neighbors(G, root))                      # Xj_tilde := {xj : j < i}
        #     for j in range(i): Xj_tilde.append(X_list[j])                              # Append vertices already seen into Xj_tilde

        #     Vi = not_N.copy()
        #     for v in Xj_tilde:                                                         # Perform set-minus operation to construct final Vi
        #         if v in not_N: Vi.remove(v)

        #     for v in V:                                                                # Append current X and I candidates (Backtracking P-1)
        #         cond1, cond2 = v not in Vi, v is not root
        #         if cond1 and cond2: X.append(v)
        #     I.append(root)

        #     Gt = nx.induced_subgraph(G, Vi)                                            # Make an induces subgraph on Vis

        #     time.sleep(self.timer)

        #     lvl += 1                                                                  
        #     self.branch_scheme_helper(Gt, I, X, lvl, W)                                # Call recursive case on ISG of G, I, X (Update level entry - Backtracking P-1.5)
        #     lvl -= 1

        #     for v in V:                                                                # Remove current X and I candidates (Backtracking P-2)
        #         cond1, cond2 = v not in Vi, v is not root
        #         if cond1 and cond2: X.remove(v)
        #     I.remove(root)

        #     time.sleep(self.timer)                                                     # Pause terminal - meant to debug code / read terminal

        # return
    
    def branch_scheme(self, G : nx):
        W = {}
        for v in G.nodes: W[v] = randint(0, 10)
        self.branch_scheme_helper(G, [], [], 0, W)

    def disp_final_sets(self):
        print(f"\nBase Set: {self.base_mis}")
        for index, cand_list in self.curr_mis_collection.items():
            print(f"Index: {index} | Set: {cand_list}")