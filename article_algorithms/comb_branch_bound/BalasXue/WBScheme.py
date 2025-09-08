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

        elif case == 2: 
            # print("Executing: Weighted Chordal Method ...\n")
            WCM = WCMethod(G, self.W)
            WCM.wc_method()
            U, S = WCM.gen_sets()

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

    def generate_neigborhood(self, G, VnU_list, v):
        V_local = list(nx.non_neighbors(G, v))
        return V_local

    def branch_scheme_helper(self, G, case):
        mis_local = []                              # Collection of maximum independent sets local to a node. 

        # Step 1: Find U \subset V such that alpha(G[U]) <= |S|.
        U, S = self.preprocess_sets(G, case)

        # Step 2: Arrange vertices in V\U as x1, ..., xn.
        VnU_list = self.arrange_list(G, U)

        # Step 3 - Case 1: If V\U is empty, return I \cup S. Otherwise, continue.
        if len(VnU_list) == 0: return S
        mis_local.append(S)

        for idx, v in enumerate(VnU_list):
            V_local = list(self.generate_neigborhood(G, VnU_list, v))
            G_local = nx.induced_subgraph(G, V_local)

            self.curr_lvl = self.curr_lvl + 1

            cand_list = self.branch_scheme_helper(G_local, case)
            cand_list.append(v)
            mis_local.append(cand_list)

            self.curr_lvl = self.curr_lvl - 1

        # Find the maximum weighted independent set and return from here.
        curr_mis, mis_weight = [], -1
        for curr_set in mis_local:
            curr_weight = 0
            for v in curr_set: curr_weight = curr_weight + self.W[v]
            if curr_weight > mis_weight:
                curr_mis, mis_weight = curr_set.copy(), curr_weight

        return curr_mis
    
    def branch_scheme(self, 
                      G     : nx,
                      W     : dict, 
                      case  : int): 
        self.W = W
        return self.branch_scheme_helper(G, case)
        # print(f"Final Output: {self.mis_list}")

    def get_wmis_collection(self): return {}
