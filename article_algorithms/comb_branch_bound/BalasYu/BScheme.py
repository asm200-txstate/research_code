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
        self.timer = 15                                                                    # Pause the output terminal
        self.VnU_index = -1
        self.VnU_S_set = []

        self.base_S = []
        self.curr_mis_collection = {}

        self.method_case = -1
    
    def branch_scheme_helper(self, 
                            G : nx, 
                            I : list, 
                            X : list, 
                            lvl : int, 
                            W : dict):

        if list(G.nodes) == []: 
            print("Null graph, returning to main ....")
            return

        # Step 1: For a graph G and independent set S \subset U, find U \subset V such that alpha(G[U]) <= |S|.

        if self.method_case == 1: 
            MChordal = ChordalMethod(G)                                                                    
            MChordal.execute_cm()
            U, S = MChordal.gen_sets()   
            if lvl == 0: self.base_S = S

        return

        # Step 2: Sort vertices in V\U - sort techniques will be updated later.

        VnU_dict = {v : G.degree(v) for v in V if v not in U}
        VnU_list = list(dict(sorted(VnU_dict.items(), key = lambda item : item[1])).keys())  

        # Case 1: There are no vertices in the V\U list.  
        if VnU_list == []: 
            # print("Here in the empty case (V\U = \emptyset) ...")
            return 
        
        # Case 2 and 3: Checking if we're at the base level.

        if lvl == 0 and VnU_list != []:  
            print(f"Level 0 set S: {S}")
            print(f"VnU List: {VnU_list}\n")

        elif lvl == 1 and VnU_list != []: 
            print(f"Level 1 Set S: {S}")
            print(f"VnU List: {VnU_list}\n")
        
        return

        V = list(G.nodes)                                                                 # Collect the whole set of vertices in G.
        if V == []: 
            print("Here in the empty set ...")
            print(f"Final sets:")
            print(f"Set S: {self.base_mis}")
            print(f"Set I: {I}")
            print(f"Set X: {X}\n")
            return

        # Step 1: Given a graph G and an independnet set S, find a subset of S, called U, where alpha(G[U]) <= |S|

        MChordal = ChordalMethod(G)                                                       # Applying Chordal Method to G                
        MChordal.execute_cm()
        U, S = MChordal.gen_sets()   

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

        cc_model = CCIP(G, list(nx.find_cliques(G))) 
        cc_model.optimize()

        # Step 2: Sort vertices in V\U by degree of vertices - sort techniques will be updated later

        VnU = {v : G.degree(v) for v in V if v not in U}
        X_list = list(dict(sorted(VnU.items(), key = lambda item : item[1])).keys())  

        # print(f"\nmis(G[U]) = {mis_model.opt_cost()}")
        # print(f"mcc(G[U]) = {cc_model.opt_cost()}\n")
        # print(f"VnU List: {X_list}\n")

        # print(f"V list: {V}")
        # print(f"U list: {U}")

        # Note: If we've reached the case that all vertices are in U and V, we're done! 
        if X_list == []:
            print("*****")
            print(f"Hit the VnU emptyset! - Root Index: {self.VnU_index}")
            print(f"Final S set: {self.VnU_S_set}")
            print(f"Current S set: {S}")
            print("*****")
            print(f"X List: {X}")
            print(f"I List: {I}")
            print("*****\n")

            # We check if we're at a level that's not -1
            if self.VnU_index != -1: 
                temp_set = self.VnU_S_set.copy()
                temp_set.append(self.VnU_index)
                if self.VnU_index not in self.curr_mis_collection:                        # Index has not been seen set 
                    self.curr_mis_collection[self.VnU_index] = temp_set       
                elif len(self.curr_mis_collection[self.VnU_index]) > len(temp_set):       # Index has been seen in set, check if the
                    self.curr_mis_collection[self.VnU_index] = temp_set                   # candidate set better/larger than the current set.
                
        if lvl == 0 and X_list != []:  
            print(f"Level 0: ")
            print(f"VnU List: {X_list}")
            print(f"Set S: {S}\n")
            self.base_mis = S

        elif lvl == 1 and X_list != []: print(f"Level 1 Set S: {S}\n")

        for i in range(len(VnU)):                                                         # Step 3: Construct Vi and apply recursive step 
            root = X_list[i]

            # print(f"Here at {root}")

            if lvl == 0: self.VnU_index = root
            elif lvl == 1: self.VnU_S_set = S

            Xj_tilde, not_N = [], list(nx.non_neighbors(G, root))                         # Xj_tilde := {xj : j < i}
            for j in range(i): Xj_tilde.append(X_list[j])                                 # Append vertices already seen into Xj_tilde

            Vi = not_N.copy()
            for v in Xj_tilde:                                                            # Perform set-minus operation to construct final Vi
                if v in not_N: Vi.remove(v)

            for v in V:                                                                   # Append current X and I candidates (Backtracking P-1)
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X.append(v)
            I.append(root)

            Gt = nx.induced_subgraph(G, Vi)                                               # Make an induces subgraph on Vis

            time.sleep(self.timer)

            lvl += 1                                                                  
            self.branch_scheme_helper(Gt, I, X, lvl, W)                                   # Call recursive case on ISG of G, I, X (Update level entry - Backtracking P-1.5)
            lvl -= 1

            for v in V:                                                                   # Remove current X and I candidates (Backtracking P-2)
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X.remove(v)
            I.remove(root)

            time.sleep(self.timer)                                                        # Pause terminal - meant to debug code / read terminal

        return
    
    def branch_scheme(self, 
                      G : nx, 
                      case : int):
        W = {}
        for v in G.nodes: W[v] = randint(0, 10)

        self.method_case = case

        self.branch_scheme_helper(G, [], [], 0, W)

        mis_model = MISIP(G)
        mis_model.optimize()
        print(f"Size of Optimal MIS: {mis_model.opt_cost()}")
        print(f"Base Set: {self.base_S}")
        print(f"Final output: {self.curr_mis_collection}")
        for curr_set in self.curr_mis_collection.values():
            pass

    def disp_final_sets(self):
        print(f"Base Set: {self.base_S}\n")
        for index, cand_list in self.curr_mis_collection.items():
            print(f"Index: {index} | Set: {cand_list}")