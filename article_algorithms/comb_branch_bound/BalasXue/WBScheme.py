import sys
import networkx as nx

from .WMISIP import WMISIP
from .WGreedyMethod import WGMethod
from .WChordalMethod import WCMethod

from BalasYu.MISIP import MISIP

class BXWBScheme:
    def __init__(self):
        self.W = None
        self.curr_lvl = 0

    def preprocess_sets(self, G, case):
        U, S = [], []

        if case == 1:
            # print("\nExecuting: Weighted Greedy Method ...\n")
            WGM = WGMethod(G, self.W)
            WGM.wg_method()
            U, S = WGM.gen_sets()
            # print(f"U: {U}")
            # print(f"S: {S}")

        elif case == 2: 
            # print("Executing: Weighted Chordal Method ...\n")
            WCM = WCMethod(G, self.W)
            WCM.wc_method()
            U, S = WCM.gen_sets()
            # print(f"V: {G.nodes}")
            # print(f"E: {G.edges}")
            # print(f"U: {U}")
            # print(f"S: {S}")
            # print(f"I: {self.I}")

        else: 
            print("Invalid output, error in code ...")
            sys.exit()

        # Step 1: Check if w(a(G[U])) <= w(S) after applying weighted chordal/greedy method. 

        # Step 1 - Part 1: Compute alpha_{w}(G[U])
        wmis_model = WMISIP(nx.induced_subgraph(G, U), self.W)
        wmis_model.optimize()
        alpha_Gw = wmis_model.opt_cost()

        # Step 1 - Part 2: Show that alpha_{w}(G[U]) <= |S|, otherwise, terminate the program. 
        S_weight = 0
        for v in S: S_weight += self.W[v]
        # print(f"\nResult: {'w(a(G[U])) <= w(S)' if alpha_Gw <= S_weight else 'w(a(G[U])) > w(S)'}\n")

        if alpha_Gw > S_weight: 
            print("\nInvalid output, error in code ...")
            sys.exit()

        return U, S
    
    def arrange_list(self, G, U):
        NW_dict = {}

        for v in G.nodes:                                           # Order vertices by sum of weights in N(v)
            Nv = nx.neighbors(G, v)

            N_weight = 0
            for u in Nv: N_weight = N_weight + self.W[u]
            NW_dict[v] = N_weight                                   # Order vertices by sum of weights in N(v)

        # Step 2: Sort vertices in V\U by the degree of their nodes. 
        VnU = {v : NW_dict[v] for v in G.nodes if v not in U}
        VnU_list = list(dict(sorted(VnU.items(), key = lambda item : item[1])).keys())

        return VnU_list
    
    def append_I(self, v):
        self.I.append(v)
        if v in self.X: self.X.remove(v)
        pass

    def remove_I(self, v):
        self.I.remove(v)
        pass

    def update_X(self, VnU_list, v):
        self.X.append(v)
        pass

    def generate_neigborhood(self, G, VnU_list, v):
        V_local = list(nx.non_neighbors(G, v))

        for u in self.X:
            if u in V_local: V_local.remove(u)
        return V_local

    def branch_scheme_helper(self, G, case):
        mis_local = []                              # Collection of maximum independent sets local to a node. 

        # Step 1: Find U \subset V such that alpha(G[U]) <= |S|.
        U, S = self.preprocess_sets(G, case)

        # Step 2: Arrange vertices in V\U as x1, ..., xn.
        VnU_list = self.arrange_list(G, U)
        # print(f"VnU list: {VnU_list}\n")

        # Step 3 - Case 1: If V\U is empty, return I \cup S. Otherwise, continue.
        if len(VnU_list) == 0: 
            # print(f"Here at a leaf for level {self.curr_lvl} - {S}") 
            return S
            # IS_union = list(set(self.I).union(S))
            # print(f"Here at a leaf for level {self.curr_lvl} - {IS_union}\n")
            # return IS_union
        
        # self.mis_list.append(S)
        mis_local.append(S)

        # S = list(set(S).union(self.I))
        
        for idx, v in enumerate(VnU_list):
            self.append_I(v)
            V_local = list(self.generate_neigborhood(G, VnU_list, v))
            # print(f"Level: {self.curr_lvl}, Index: {idx} (Vertex {v}) - V_local: {V_local}\n")

            G_local = nx.induced_subgraph(G, V_local)

            self.curr_lvl = self.curr_lvl + 1

            cand_list = self.branch_scheme_helper(G_local, case)
            cand_list.append(v)
            mis_local.append(cand_list)

            # mis_local.append(self.branch_scheme_helper(G_local, case))
            self.curr_lvl = self.curr_lvl - 1

            # self.update_X(VnU_list, v)
            self.remove_I(v)

            # print("After:")
            # print(f"I: {self.I}")
            # print(f"X: {self.X}")
            # print(f"V_local: {V_local}\n")

        # print(f"\nI: {self.I}")
        # print(f"X: {self.X}\n")

        # mis_local.remove(S)
        # mis_local.append(list(set(S).union(self.I)))

        # print(f"Local Listing at Level {self.curr_lvl}:")
        # for curr_set in mis_local:
        #     print(curr_set)
        # print()

        # Find the maximum weighted independent set and return from here.
        curr_mis, mis_weight = [], -1
        for curr_set in mis_local:
            curr_weight = 0
            for v in curr_set: curr_weight = curr_weight + self.W[v]
            # print(f"curr_set: {curr_set} - weight: {curr_weight}")
            if curr_weight > mis_weight:
                curr_mis, mis_weight = curr_set.copy(), curr_weight
                # print(f"New curr_mis = {curr_mis}")

        # mis_local.remove(S)
        # mis_local.append(list(set(curr_mis).union(self.I)))
        # print(f"\nLocal Output: {mis_local}\n") 
        # if curr_mis == S: curr_mis = list(set(curr_mis).union(self.I))
        return curr_mis
    
    def branch_scheme(self, 
                      G     : nx,
                      W     : dict, 
                      case  : int): 
        self.W = W
        return self.branch_scheme_helper(G, case)
        # print(f"Final Output: {self.mis_list}")

    def get_wmis_collection(self): return {}
