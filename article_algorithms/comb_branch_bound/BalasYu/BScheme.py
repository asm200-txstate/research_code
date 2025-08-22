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

from .RecSimpFix import RSF
from .MISIP import MISIP
from .CCIP import CCIP
from .GreedyMethod import GMethod
from .ChordalMethod import ChordalMethod

from BalasXue.WChordalMethod import WCMethod

class BYBScheme:
    def __init__(self):
        self.VnU_index = -1
        self.VnU_S_set = []                                 # Base VnU set

        self.base_S = []                                    # Base independent set S on the root case. 
        self.mis_collection = {}                            # The collection of independent sets at level 0 that are maximum independent sets to G[Vi] (See Paper, Paragraph 1 - Page 4)

        self.method_case = -1

    def branch_scheme_helper(self, 
                            graph : nx, 
                            curr_mis : list,
                            I_inc_list : list, 
                            X_exc_list : list, 
                            curr_lvl : int, 
                            lvl_0_idx : int,
                            weight_dict : dict):
        
        # print(f"Graph Vertices: {graph.nodes}")

        if list(graph.nodes) == []: 
            print("Null graph, returning ....")
            # print(f"Level 0 vertex: {lvl_0_idx}")
            # print(f"I set: {I_inc_list}")
            # print(f"X set: {X_exc_list}")

            if lvl_0_idx not in self.mis_collection: self.mis_collection[lvl_0_idx] = I_inc_list
            elif len(self.mis_collection[lvl_0_idx]) < len(I_inc_list): self.mis_collection[lvl_0_idx] = I_inc_list

            return

        # Step 1: For a graph G and independent set S \subset U, find U \subset V such that alpha(G[U]) <= |S|.

        if self.method_case == 1: 
            MChordal = ChordalMethod(graph)                                                                    
            MChordal.execute_cm()
            U, S = MChordal.gen_sets()   
            if curr_lvl == 0: self.base_S = S
        
        elif self.method_case == 2: 
            MGreedy = GMethod(graph)    
            MGreedy.greedy_cc()
            U, S = MGreedy.gen_sets()
            if curr_lvl == 0: self.base_S = S

        # Step 2: Sort vertices in V\U - sort techniques will be updated later.

        VnU_dict = {v : graph.degree(v) for v in graph.nodes if v not in U}
        VnU_list = list(dict(sorted(VnU_dict.items(), key = lambda item : item[1])).keys())  

        # Case 1: The set V\U is an empty set
        if VnU_list == []:
            print("Here in the empty case V \ U = [] ...")
            print(f"Level 0 vertex: {lvl_0_idx}")
            # print(f"I set: {I_inc_list}")
            # print(f"X set: {X_exc_list}")
            # print(f"S set: {S}\n")
            # print(f"MIS set: {curr_mis}\n")

            output = list(set(I_inc_list).union(S))
            if lvl_0_idx not in self.mis_collection: self.mis_collection[lvl_0_idx] = output
            elif len(self.mis_collection[lvl_0_idx]) < len(output): self.mis_collection[lvl_0_idx] = output

            return

        # Case 2: The set V\U is a nonempty set 
        if curr_lvl == 0:
            # print(f"Level 0 set S: {S}")
            # print(f"VnU List: {VnU_list}\n")
            self.VnU_S_set = VnU_list

        V = list(graph.nodes)
        if V == []:
            print("Here in a null graph ...\n")

        for idx in range(len(VnU_list)):
            print(f"Index: {idx} - Node: {VnU_list[idx]}\n")

            if curr_lvl == 0: 
                lvl_0_idx = VnU_list[idx]                               # Track the index and it's largest independent set (so far). 
                curr_mis = [VnU_list[idx]]
                # self.mis_collection[lvl_0_idx] = [idx]                # Make a base set when starting, update later when finding a larger set. 

            notN_local = list(nx.non_neighbors(graph, VnU_list[idx]))   # Non-neighboring vertices in x_i 

            I_local, X_local = [], []
            V_local = notN_local.copy()

            # print("Before: ")
            # print(f"V_local: {V_local}")
            # print(f"X_local: {X_local}")
            # print(f"I_local: {I_local}")

            I_local.append(VnU_list[idx])
            for jdx in range(idx): X_local.append(VnU_list[jdx])        # Append vertices already seen into Xj_tilde

            IXlocal_union = list(set(X_local).union(I_local))
            for u in IXlocal_union:
                if u in V_local: V_local.remove(u)

            # print("\nAfter: ")
            # print(f"V_local: {V_local}")
            # print(f"X_local: {X_local}")
            # print(f"I_local: {I_local}\n")

            if len(V_local) == 0: 
                print("Output is going to be empty ...")
                # print(f"Set S: {S}")

            X_exc_list = list(set(X_exc_list).union(X_local))
            I_inc_list = list(set(I_inc_list).union(I_local))

            # print(f"X_exc_list: {X_exc_list}")
            # print(f"I_inc_list: {I_inc_list}\n")

            g_update = nx.induced_subgraph(graph, V_local)

            self.branch_scheme_helper(g_update, curr_mis, I_inc_list, X_exc_list, curr_lvl + 1, lvl_0_idx, weight_dict)

            X_exc_list = list(set(X_exc_list).difference(X_local))
            I_inc_list = list(set(I_inc_list).difference(I_local))

        return

        VnU_dict = {v : graph.degree(v) for v in V if v not in U}
        VnU_list = list(dict(sorted(VnU_dict.items(), key = lambda item : item[1])).keys())  

        # Case 1: There are no vertices in the V\U list.  
        if VnU_list == []: 
            # print("Here in the empty case (V\U = \emptyset) ...")
            return 
        
        # Case 2 and 3: Checking if we're at the base level.

        if curr_lvl == 0 and VnU_list != []:  
            print(f"Level 0 set S: {S}")
            print(f"VnU List: {VnU_list}\n")

        elif curr_lvl == 1 and VnU_list != []: 
            print(f"Level 1 Set S: {S}")
            print(f"VnU List: {VnU_list}\n")

        V = list(graph.nodes)                                                                 # Collect the whole set of vertices in G.
        if V == []: 
            print("Here in the empty set ...")
            print(f"Final sets:")
            print(f"Set S: {self.base_mis}")
            print(f"Set I: {I_inc_list}")
            print(f"Set X: {X_exc_list}\n")
            return

        # Step 1: Given a graph G and an independnet set S, find a subset of S, called U, where alpha(G[U]) <= |S|

        MChordal = ChordalMethod(graph)                                                       # Applying Chordal Method to G                
        MChordal.execute_cm()
        U, S = MChordal.gen_sets()   

        # # MGreedy = GMethod(graph)
        # # MGreedy.greedy_cc()
        # # U, S = MGreedy.gen_sets()

        # # Note to reader: Wouldn't make sense since you're looking at the weights themselves and not the vertices in the set. 
        # # MWChordal = WCMethod(graph, weight_dict)
        # # MWChordal.wc_method()
        # # U, S = MWChordal.gen_sets()

        # print(f"U set : {U}")
        # print(f"S set : {S}")

        mis_model = MISIP(nx.induced_subgraph(graph, U))
        mis_model.optimize()

        cc_model = CCIP(graph, list(nx.find_cliques(graph))) 
        cc_model.optimize()

        # Step 2: Sort vertices in V\U by degree of vertices - sort techniques will be updated later

        VnU = {v : graph.degree(v) for v in V if v not in U}
        X_list = list(dict(sorted(VnU.items(), key = lambda item : item[1])).keys())  

        # print(f"\nmis(graph[U]) = {mis_model.opt_cost()}")
        # print(f"mcc(graph[U]) = {cc_model.opt_cost()}\n")
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
            print(f"X List: {X_exc_list}")
            print(f"I List: {I_inc_list}")
            print("*****\n")

            # We check if we're at a level that's not -1
            if self.VnU_index != -1: 
                temp_set = self.VnU_S_set.copy()
                temp_set.append(self.VnU_index)
                if self.VnU_index not in self.mis_collection:                        # Index has not been seen set 
                    self.mis_collection[self.VnU_index] = temp_set       
                elif len(self.mis_collection[self.VnU_index]) > len(temp_set):       # Index has been seen in set, check if the
                    self.mis_collection[self.VnU_index] = temp_set                   # candidate set better/larger than the current set.
                
        if curr_lvl == 0 and X_list != []:  
            print(f"Level 0: ")
            print(f"VnU List: {X_list}")
            print(f"Set S: {S}\n")
            self.base_mis = S

        elif curr_lvl == 1 and X_list != []: print(f"Level 1 Set S: {S}\n")

        for i in range(len(VnU)):                                                         # Step 3: Construct Vi and apply recursive step 
            root = X_list[i]

            # print(f"Here at {root}")

            if curr_lvl == 0: self.VnU_index = root
            elif curr_lvl == 1: self.VnU_S_set = S

            Xj_tilde, not_N = [], list(nx.non_neighbors(graph, root))                         # Xj_tilde := {xj : j < i}
            for j in range(i): Xj_tilde.append(X_list[j])                                 # Append vertices already seen into Xj_tilde

            Vi = not_N.copy()
            for v in Xj_tilde:                                                            # Perform set-minus operation to construct final Vi
                if v in not_N: Vi.remove(v)

            for v in V:                                                                   # Append current X and I candidates (Backtracking P-1)
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X_exc_list.append(v)
            I_inc_list.append(root)

            Gt = nx.induced_subgraph(graph, Vi)                                               # Make an induces subgraph on Vis

            time.sleep(self.timer)

            curr_lvl += 1                                                                  
            self.branch_scheme_helper(Gt, I_inc_list, X_exc_list, curr_lvl, weight_dict)                                   # Call recursive case on ISG of G, I, X (Update level entry - Backtracking P-1.5)
            curr_lvl -= 1

            for v in V:                                                                   # Remove current X and I candidates (Backtracking P-2)
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X_exc_list.remove(v)
            I_inc_list.remove(root)

            time.sleep(self.timer)                                                        # Pause terminal - meant to debug code / read terminal

        return
    
    def branch_scheme(self, 
                      graph : nx, 
                      case : int):
        weight_dict = {}
        for v in graph.nodes: weight_dict[v] = randint(0, 10)

        self.method_case = case
        self.branch_scheme_helper(graph, [], [], [], 0, 0, weight_dict)

    def mis_status(self, graph : nx):
        if list(graph.nodes) == []: 
            print("\nNull graph, no such optimal MIS exists ...\n")
            return

        status_list = []

        mis_model = MISIP(graph)
        mis_model.optimize()

        print(f"\nExpected Optimal MIS Size: {mis_model.opt_cost()}\n")
        print(f"Base Set     | Length: {len(self.base_S):>5} | Status: {mis_model.opt_cost() == len(self.base_S)}")
        for idx, curr_set in self.mis_collection.items():
            print(f"Index: {idx:>5} | Length: {len(curr_set):>5} | Status: {mis_model.opt_cost() == len(curr_set)}")
            status_list.append(mis_model.opt_cost() == len(curr_set))

        status_list.append(mis_model.opt_cost() == len(self.base_S))    # Appending the base case 

        # Displaying the final outcome to the terminal 
        if any(status_list): print("\nOptimal MIS set was found\n")
        else: print("\nOptimal MIS set was not found\n")

    def get_mis_collection(self): return self.mis_collection