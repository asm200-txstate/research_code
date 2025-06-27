## ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** 
## Filename: GreedyMethod.py   
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

from networkx.algorithms.approximation.clique import max_clique

from .MISIP import MISIP

class GreedyMethod():
    def __init__(self, G): 
        self.G = G
        self.mis_model = MISIP(G)
        self.mis_model.optimize()
        self.S = self.mis_model.opt_soln()
    
    def greedy_cc(self):
        K_list, Gt = [[] for _ in range(len(self.S))], self.G 
        for idx, v in enumerate(self.S):
            neighbors = nx.neighbors(Gt, v)                          
            Gv = nx.induced_subgraph(self.G, neighbors)                      # Get the induced subgraph G[N[v]].

            clique = list(max_clique(Gv))                               # Get the largest clique in the list - greedy process (selecting vertices that maintain simplicial ordering on v)
            clique.append(v)                                            # Append the vertex v into the list. 
            clique = set(clique)

            nodes = set(Gt.nodes)
            node_update = list(nodes.difference(clique))                # Update the node list to generate a new induced subgraph. 

            Gt = nx.induced_subgraph(Gt, node_update)                   # Generate the induced subgraph with the subset of vertices

            clique = list(clique)
            K_list[idx] = clique

        return [v for list in K_list for v in list]

    def gen_sets(self):
        U = self.greedy_cc()
        return U, self.S

    # # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # # Method Name: N/A
    # #
    # # Description: N/A
    # #
    # # Argument(s): N/A
    # #
    # # Return(s): N/A
    # # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # def greedy_method(self, G : nx):
    #     mis_model = MISIP(G)
    #     mis_model.optimize()
    #     S = mis_model.opt_soln()

    #     # Greedy clique-covering algorithm 
    #     K_list, Gt = [[] for _ in range(len(S))], G 
    #     for idx, v in enumerate(S):
    #         neighbors = nx.neighbors(Gt, v)                          
    #         Gv = nx.induced_subgraph(G, neighbors)                      # Get the induced subgraph G[N[v]].

    #         clique = list(max_clique(Gv))                               # Get the largest clique in the list - greedy process (selecting vertices that maintain simplicial ordering on v)
    #         clique.append(v)                                            # Append the vertex v into the list. 
    #         clique = set(clique)

    #         nodes = set(Gt.nodes)
    #         node_update = list(nodes.difference(clique))                # Update the node list to generate a new induced subgraph. 

    #         Gt = nx.induced_subgraph(Gt, node_update)                   # Generate the induced subgraph with the subset of vertices

    #         clique = list(clique)
    #         K_list[idx] = clique

    #     for idx in range(len(K_list)): print(f"List {idx}: {K_list[idx]}")

    #     U = [v for list in K_list for v in list]
    #     print(f"U list: {U}")

    #     return S, U