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
from random import shuffle

from .RecSimpFix import RSF
from .MISIP import MISIP
from .CCIP import CCIP

from Graph.GraphPlot import GraphPlot

class CMethod:
    def __init__(self, 
                 G : nx
                 ): 
        self.graph_comp = nx.complement(G)
        self.U, self.S = [], []
        self.graph = G

        self.label_dict = {}
        self.rank_dict = {}
        self.seen_list = []
        self.sigma_t = []
        self.T = []

        for v in self.graph.nodes: self.label_dict[v] = []

    def choose_vertex(self):
        max_list, max_len = [], -1
        for u_node, u_list in self.label_dict.items():
            if u_list == []: continue 
            elif len(u_list) >= max_len and u_node not in self.seen_list:
                if len(self.label_dict[u_node]) == max_len: max_list.append(u_node)
                else: 
                    max_list = []
                    max_list.append(u_node)
                    max_len = len(self.label_dict[u_node])
        
        if len(max_list) == 0: return min(self.graph.nodes)
        elif len(max_list) == 1: return max_list[0]
        return min(max_list)
    
    def is_adjacent(self, 
                    w : int, 
                    isgraph : nx
                    ):
        vertex_list = isgraph.nodes
        for v in vertex_list:
            if v == w: continue
            if (v, w) not in isgraph.edges(): return False
        return True

    def is_quasi_simplicial(self, 
                            v : int, 
                            graph_t : nx
                            ):

        successor_list = [u for u in self.sigma_t if u in nx.neighbors(graph_t, v)]
        if successor_list == []: return True

        w = successor_list[0]
        return self.is_adjacent(w, nx.induced_subgraph(graph_t, successor_list))

    def find_mtis(self):
        for i in range(len(self.graph_comp.nodes) - 1, -1, -1): 
            v = self.choose_vertex()
            isgraph = nx.induced_subgraph(self.graph_comp, list(set(self.T).union([v])))
            if self.is_quasi_simplicial(v, isgraph):
                if v not in self.T: self.T.append(v)
                self.sigma_t.insert(0, v)

            self.rank_dict[v] = i
            self.seen_list.append(v)
            
            curr_list = list(set(nx.neighbors(self.graph_comp, v)).difference(self.sigma_t))

            for u in list(set(nx.neighbors(self.graph_comp, v)).difference(self.sigma_t)):
                self.rank_dict[u] = i-1
                self.label_dict[u].append(i)

    def execute_cm(self):
        if list(self.graph_comp.nodes) == []: return

        is_connected = nx.is_connected(self.graph_comp) # Check if the complement of the graph is chordal or not. 
        if is_connected: self.find_mtis()
        else: 
            temp_T = []
            orig_G = self.graph.copy()
            orig_Gc = self.graph_comp.copy()
            components = list(nx.connected_components(self.graph_comp))
            
            # Iterate through each component and find a subset of vertices that makes it chordal. 
            for comp in components: 
                self.graph = nx.induced_subgraph(orig_G, comp)
                self.graph_comp = nx.induced_subgraph(orig_Gc, comp)
                self.find_mtis()
                temp_T.append(self.T)
                self.T = []
            
            # Merge the final sublists of vertices to make one set that makes the non-connected graph chordal. 
            merged_T = []
            for curr_list in temp_T: merged_T.extend(curr_list)
            self.graph = orig_G
            self.graph_comp = orig_Gc

        # Step 2: Find an independent set S to G[T]
        Gt = nx.induced_subgraph(self.graph, self.T)
        mis_model = MISIP(Gt)
        mis_model.optimize()
        self.S = mis_model.opt_soln()

        # Step 3: Find the minimum clique cover for the graph G
        clique_list = list(nx.find_cliques(Gt))
        MCC_model = CCIP(Gt, clique_list)
        MCC_model.optimize()
        K = MCC_model.opt_soln()

        # Step 3.5 P2: Generate a clique dictionary from the original clique K
        clique_dict = {}
        for idx, k in enumerate(K): clique_dict[idx] = k.copy()

        # Step 4: Append vertices from V\T to the cliques in clique_dict
        VnT = list(set(self.graph.nodes).difference(self.T))

        for v in VnT: 
            neighborhood = list(self.graph.neighbors(v))
            for idx, clique in clique_dict.items():
                C_set, N_set = set(clique), set(neighborhood) 
                if C_set.issubset(N_set): 
                    clique_dict[idx].append(v) 
                    continue 
        
        # Step 4.5: Store updated cliques from clique_dict to K_hat list
        K_hat = []
        for clique in clique_dict.values():
            K_hat.append(clique)

        # Step 5: Unionize the vertices in K_hat to the set U
        self.U = set([])
        for clique in K_hat:
            for v in clique: self.U.add(v)
        self.U = sorted(list(self.U))

        # Step 5.5: Check that \alpha(G[U]) <= |S|
        mis_model = MISIP(nx.induced_subgraph(self.graph, self.U))
        mis_model.optimize()
        final_S = mis_model.opt_soln()

        # graph_comp = nx.complement(nx.induced_subgraph(self.graph, self.T))

        # print(f"\nalpha(G[U]): {len(final_S)} | |S|: {len(self.S)}")
        # print(f"Final set T: {self.T}\n")
        
    def gen_sets(self): return self.U, self.S

    def is_chordal(self): 
        if self.T != []: return nx.is_chordal(nx.induced_subgraph(nx.complement(self.graph), self.T))
        else: return True

    def T_vertices(self): return self.T