import sys
import networkx as nx

from .WMISIP import WMISIP
from .WGreedyMethod import WGMethod
from .WChordalMethod import WCMethod

from BalasYu.MISIP import MISIP

class BXWBScheme:
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
                             weight_dict : dict, 
                             case : int):
        
        # Step 1: For a graph G and independent set S \subset U, 
        # find U \subset V such that alpha(G[U]) <= |S|.

        if case == 1:
            print("Executing: Weighted Greedy Method ...\n")
            WGM = WGMethod(graph, weight_dict)
            WGM.wg_method()
            U, S = WGM.gen_sets()
            K_list = WGM.gen_cliques()
            W_dict = WGM.gen_weights()
        else: 
            print("Executing: Weighted Chordal Method ...\n")
            WCM = WCMethod(graph, weight_dict)
            WCM.wc_method()
            U, S = WCM.gen_sets()
            K_list = WCM.gen_cliques()
            W_dict = WCM.gen_clique_weights()

            # for idx in range(len(K_list)):
            #     print(f"K_list: {K_list[idx]}")
            #     print(f"W_dict: {W_dict[idx]}\n")

            # Task: Generate a method where you return the new cliques and the respective weights. 
            # return

        # print(f"len(S):      {len(S)}")
        # print(f"len(U):      {len(U)}")
        # print(f"len(K):      {len(K_list)}")
        # print(f"len(W_dict): {len(W_dict)}")

        wmis_model = WMISIP(nx.induced_subgraph(graph, U), weight_dict)
        wmis_model.optimize()

        S_weight = 0
        for v in S: S_weight += weight_dict[v]
        print(f"Result: {'weight(a(G[U])) <= w(S)' if wmis_model.opt_cost() <= S_weight else 'weight(a(G[U])) > w(S)'}\n")

        if wmis_model.opt_cost() > S_weight: 
            print("Invalid output, error in code ...")
            sys.exit()

        NW_dict = {}                                                   # Neighborhood weight dictionary
        for v in graph.nodes:                                          # Order vertices by sum of weights in N(v)
            Nv = nx.neighbors(graph, v)

            N_weight = 0
            for u in Nv: N_weight = N_weight + weight_dict[u]
            NW_dict[v] = N_weight

        # Step 2: Sort vertices in V\U
        VnU = {v : NW_dict[v] for v in graph.nodes if v not in U}
        VnU_list = list(dict(sorted(VnU.items(), key = lambda item : item[1])).keys())

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
        if V == []: print("Here in a null graph ...\n")

        # Step 3: Execute the branch and bound scheme similar to the Balas & Yu algorithm. 
        for idx, v in enumerate(VnU_list):
            print(f"Index: {idx} - Node: {v}\n")

            if curr_lvl == 0: 
                lvl_0_idx = v                               # Track the index and it's largest independent set (so far). 
                curr_mis = [v]
                # self.mis_collection[lvl_0_idx] = [idx]    # Make a base set when starting, update later when finding a larger set. 

            notN_local = list(nx.non_neighbors(graph, v))   # Non-neighboring vertices in x_i 

            I_local, X_local = [], []
            V_local = notN_local.copy()

            I_local.append(v)
            for jdx in range(idx): X_local.append(VnU_list[jdx])        # Append vertices already seen into Xj_tilde

            IXlocal_union = list(set(X_local).union(I_local))
            for u in IXlocal_union:
                if u in V_local: V_local.remove(u)

            # if len(V_local) == 0: print("Output is going to be empty ...\n")

            X_exc_list = list(set(X_exc_list).union(X_local))
            I_inc_list = list(set(I_inc_list).union(I_local))

            # print(f"X_exc_list: {X_exc_list}")
            # print(f"I_inc_list: {I_inc_list}\n")

            g_update = nx.induced_subgraph(graph, V_local)

            self.branch_scheme_helper(g_update, curr_mis, I_inc_list, X_exc_list, curr_lvl+1, lvl_0_idx, weight_dict, case)

            X_exc_list = list(set(X_exc_list).difference(X_local))
            I_inc_list = list(set(I_inc_list).difference(I_local))

        return

    def branch_scheme(self, G : nx, W : dict, case : int): 
        # self.branch_scheme_helper(G, W, [], [], 0, case)
        self.branch_scheme_helper(G, [], [], [], 0, 0, W, case)

    def get_mis_collection(self): return self.mis_collection