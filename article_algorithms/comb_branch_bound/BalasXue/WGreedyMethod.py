import sys

from .WMISIP import WMISIP

from random import choice
import networkx as nx

class WGMethod:
    def __init__(self, G : nx, W : dict): 
        self.graph = G
        self.weights = W

        self.U = []
        self.S = []
        self.K_list = []
        self.W_list = []

    def maximal_clique(self, curr_V : list): 
        graph_comp = nx.complement(nx.induced_subgraph(self.graph, curr_V))
        V, I = list(graph_comp.nodes), []

        while V != []:
            v = choice(V)
            I.append(v)
            
            neighborhood = graph_comp.neighbors(v)
            V.remove(v)

            for v in neighborhood:
                if v in V: V.remove(v)
        
        return I

    def wg_method(self): 
        wmis_model = WMISIP(self.graph, self.weights)
        wmis_model.optimize()
        self.S = wmis_model.opt_soln()

        S_weight = 0
        for v in self.S: S_weight += self.weights[v]

        curr_vertices = list(self.graph.nodes)
        curr_weights = self.weights.copy()
        min_w_sum = 0
        curr_idx = 0

        self.W_list = []
        U_list = []

        print(f"Original Nodes: {list(curr_weights.keys())}")
        print(f"Original Weights: {list(curr_weights.values())}\n")

        while True:
            curr_K = self.maximal_clique(curr_vertices)
            print(f"Current clique: {curr_K}")

            self.K_list.append(curr_K)                                                           # Appending current K list

            min_W = sys.maxsize
            for v in curr_K:
                if min_W > curr_weights[v]: min_W = curr_weights[v]

            print(f"Current Sum W_min: {min_w_sum}")

            min_w_sum += min_W
            self.W_list.append(min_W)                                                            # Append current min_W to list
            
            print(f"Curr W: {min_W}")
            print(f"Curr weights: {curr_weights.copy()}")

            # Update - you're still looking at the vertices of the entire graph, not the induced version after each iteration.
            weight_update = {}
            for v in curr_vertices:
                if v in curr_K: weight_update[v] = curr_weights[v] - min_W
                else: weight_update[v] = curr_weights[v]
            curr_weights = weight_update.copy()

            U, Z = [], []
            for v in curr_vertices:
                if curr_weights[v] == 0: U.append(v)
                elif curr_weights[v] > S_weight - min_w_sum: Z.append(v)
            
            print(f"Current U: {U}")
            print(f"Current Z: {Z}")

            U_list.append(U)
            
            U_set, Z_set, V_set = set(U), set(Z), set(curr_vertices)

            UZ_union = U_set.union(Z_set)
            curr_vertices = list(V_set.difference(UZ_union))

            print(f"Updated Vertices: {curr_vertices}\n")

            curr_idx += 1
            if curr_vertices == [] or curr_idx == 15: break

        print(f"Final index: {curr_idx}")

        for U in U_list:
            for u in U: self.U.append(u)

    def gen_sets(self): return self.U, self.S

    def gen_cliques(self): return self.K_list

    def gen_weights(self): return self.W_list