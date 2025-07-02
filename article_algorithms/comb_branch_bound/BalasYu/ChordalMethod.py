## ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** 
## Filename: ChordalMethod.py   
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

import networkx as nx

from .RecSimpFix import RSF
from .MISIP import MISIP
from .CCIP import CCIP

class ChordalMethod:
    def __init__(self, G : nx): 
        self.rsf_model = RSF()
        self.U, self.S = None, None
        self.G = G

    def chordal_method(self):
        VnT, T = self.rsf_model.recursive_simplicial_fixing(self.G)

        Gc = nx.complement(self.G)
        GT = nx.induced_subgraph(self.G, T)
        ISGc = nx.induced_subgraph(Gc, T)

        mis_model = MISIP(GT)
        mis_model.optimize()
        self.S = mis_model.opt_soln()

        clique_list = list(nx.find_cliques(GT))
        MCC_model = CCIP(GT, clique_list)
        MCC_model.optimize()
        CC = MCC_model.opt_soln()

        clique_dict = {}
        for idx, clique in enumerate(clique_list): clique_dict[idx] = clique.copy()

        # for vertex in VnT: 
        #     neighborhood = list(G.neighbors(vertex))
        #     for idx in range(len(clique_list)):
        #         C_set, N_set = set(clique_dict[idx]), set(neighborhood)
        #         if C_set.issubset(N_set): clique_dict[idx].append(vertex)

        # G_cliques = list(nx.find_cliques(G))

        self.U = set([])
        for clique in clique_dict.values():
            print(f"clique: {list(clique)}")
            for v in clique: self.U.add(v)
        self.U = list(self.U)
    
    def gen_sets(self): return self.U, self.S