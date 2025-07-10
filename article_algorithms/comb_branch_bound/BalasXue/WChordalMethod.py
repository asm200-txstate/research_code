import sys
import networkx as nx
sys.dont_write_bytecode = True

from random import choice

from .WMISIP import WMISIP
from .WCCIP import WCCIP
from BalasYu.RecSimpFix import RSF

class WCMethod:
    def __init__(self, G : nx, W : dict):
        self.graph = G
        self.weights = W
        self.U, self.S = None, None

    def wc_method(self): 
        rsf_model = RSF()
        VnT, T = rsf_model.recursive_simplicial_fixing(self.graph) ## Find a way to get the maximal set, not the maximum set
        
        isg_t = nx.induced_subgraph(self.graph, T)
        wmis_model = WMISIP(isg_t, self.weights)
        wmis_model.optimize()
        self.S = wmis_model.opt_soln()

        clique_list = list(nx.find_cliques(isg_t))
        clique_weights = []
        for C in clique_list:
            weight = 0
            for v in C: weight += self.weights[v]
            clique_weights.append(weight)

        wccip_model = WCCIP(isg_t, clique_weights, clique_list)
        wccip_model.optimize()
        WCC = wccip_model.opt_soln()

        clique_dict = {}
        for idx, clique in enumerate(WCC): clique_dict[idx] = clique.copy()

        VnT = []
        for v in self.graph.nodes:
            if v not in T: VnT.append(v)

        print(f"VnT List: {VnT}")

        for vertex in VnT: 
            neighborhood = list(self.graph.neighbors(vertex))
            for idx in range(len(clique_list)):
                C_set, N_set = set(clique_dict[idx]), set(neighborhood)
                if C_set.issubset(N_set): clique_dict[idx].append(vertex)

        for clique in clique_dict.values(): print(f"Clique: {clique}")

        U = set()
        for C in clique_list:
            for v in C: U.add(v)
        self.U = list(U)

    def gen_sets(self): return self.U, self.S