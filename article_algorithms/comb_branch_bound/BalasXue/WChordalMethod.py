import sys
import networkx as nx
sys.dont_write_bytecode = True

from random import choice

from .WMISIP import WMISIP
from .WMCCIP import WMCCIP

from BalasYu.RecSimpFix import RSF
from BalasYu.ChordalMethod import ChordalMethod

class WCMethod:
    def __init__(self, G : nx, W : dict):
        self.graph = G
        self.weights = W

        self.cliques = None
        self.clique_weights = None
        self.U, self.S = None, None

    def wc_method(self): 
        ## Find a vertex-maximal induced subgraph such that \overline{G}[T] is chordal.
        CM_model = ChordalMethod(self.graph)
        CM_model.find_mtis()
        T = CM_model.T_vertices()

        ## Find the maximum independent set S on the induced subgraph G[T].
        graph_T = nx.induced_subgraph(self.graph, T)
        wmis_model = WMISIP(graph_T, self.weights)
        wmis_model.optimize()
        self.S = wmis_model.opt_soln()

        ## Create a list of weighted cliques on G[T].
        clique_list = list(nx.find_cliques(graph_T))
        clique_weights = []
        for C in clique_list:
            weight = 0
            for v in C: weight += self.weights[v]
            clique_weights.append(weight)

        ## Find the minimum clique cover to the  
        wccip_model = WMCCIP(graph_T, clique_weights, clique_list)
        wccip_model.optimize()
        min_wcc = wccip_model.opt_soln()

        ## Map an index from 0 - len(min_wcc) to a clique from the induced subgraph G[T]
        min_clique_dict = {}
        for idx, clique in enumerate(min_wcc): min_clique_dict[idx] = list(clique.copy())

        ## Find the vertices that are in V\T
        VnT = []
        for v in self.graph.nodes:
            if v not in T: VnT.append(v)

        ## Greeedily add vertices in V\T to these cliques to generate larger cliques. 
        for v in VnT: 
            neighborhood = list(self.graph.neighbors(v))
            for idx in range(len(min_clique_dict)):
                C_set = set(min_clique_dict[idx])
                N_set = set(neighborhood)
                if C_set.issubset(N_set): 
                    min_clique_dict[idx].append(v)
        
        ## Reinitializing the previous clique weights to $K_1, ..., K_{|S|}$ 
        ## to the new clique weights $\overline{K}_1, ..., \overline{K}_{|S|}$ 
        clique_weights = []
        for clique in min_clique_dict.values(): 
            clique_weight = 0
            for v in clique: 
                clique_weight = clique_weight + self.weights[v]
            clique_weights.append(clique_weight)
        
        self.cliques = list(min_clique_dict.values())
        self.clique_weights = clique_weights

        ## Unionize these sets \hat{K}_{1}, \ldots, \hat{K}_{|S|}  to generate U. 
        U = set()
        for C in clique_list:
            for v in C: U.add(v)
        self.U = list(U)

    def gen_sets(self): return self.U, self.S

    def gen_cliques(self): return self.cliques

    def gen_clique_weights(self): return self.clique_weights