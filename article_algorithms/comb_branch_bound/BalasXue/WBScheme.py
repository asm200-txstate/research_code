import networkx as nx

from .WMISIP import WMISIP

class BXWBScheme:
    def __init__(self): pass

    def branch_scheme_helper(self, G : nx, W : dict, I : list, X : list, lvl : int):

        while True: 
            if len(list(G.nodes)) != 0:  S = nx.maximal_independent_set(G)
            else: S = []
            U = None

            S_weight = 0                                                # Sum of weights on S
            for v in S: S_weight = S_weight + W[v]

            wmis_model = WMISIP(G, W)
            wmis_model.optimize()
            if wmis_model.opt_cost() <= S_weight: 
                U = wmis_model.opt_soln()
                break

        NW_dict = {}                                                   # Neighborhood weight dictionary
        for v in G.nodes:                                              # Order vertices by sum of weights in N(v)
            Nv = nx.neighbors(G, v)

            N_weight = 0
            for u in Nv: N_weight = N_weight + W[u]
            NW_dict[v] = N_weight

        VnU = {v : NW_dict[v] for v in G.nodes if v not in U}
        VnU_list = list(dict(sorted(VnU.items(), key = lambda item : item[1])).keys())

        for idx, v in enumerate(VnU_list): 
            root = v
            print(f"Current root: {v}, Index: {idx}")

            Xj_tilde, not_N = [], list(nx.non_neighbors(G, v))                      
            for jdx in range(idx): Xj_tilde.append(VnU_list[jdx])                      # Xj_tilde := {xj : j < i}

            Vi = not_N.copy()
            for v in Xj_tilde:
                if v in not_N: Vi.remove(v)

            for v in list(G.nodes):                                                    # Append current X and I candidates (Backtracking P-1)
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X.append(v)
            I.append(root)

            Gt = nx.induced_subgraph(G, Vi)                                            # Make an induces subgraph on Vis

            lvl += 1                                                                  
            self.branch_scheme_helper(Gt, W, I, X, lvl)                                # Call recursive case on ISG of G, I, X (Update level entry - Backtracking P-1.5)
            lvl -= 1

            for v in list(G.nodes):                                                    # Remove current X and I candidates (Backtracking P-2)
                cond1, cond2 = v not in Vi, v is not root
                if cond1 and cond2: X.remove(v)
            I.remove(root)

        if VnU_list == []:
            print("Final sets!")
            print(f"I: {I}")
            print(f"X: {X}")

    def branch_scheme(self, G : nx, W : dict): 
        self.branch_scheme_helper(G, W, [], [], 0)