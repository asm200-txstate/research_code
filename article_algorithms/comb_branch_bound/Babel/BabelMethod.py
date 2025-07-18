import sys
import random
import networkx as nx

from BalasXue.WMISIP import WMISIP
from BalasYu.RecSimpFix import RSF

class BMethod:
    def __init__(self, G : nx, W : dict): 
        self.graph = G
        self.weights = W
        self.clique_list = []

        self.S = []
        self.S_weight = 0

    def GKD(self):
        gkd_dict = {}
        for v in self.graph.nodes:
            non_Nv = list(nx.non_neighbors(self.graph, v))
        
            K_list = []
            for u in non_Nv:
                for K in self.clique_list:
                    if u in K and K not in K_list: K_list.append(list(K))

            gkd_dict[v] = K_list

        print(f"Clique list (so far): {self.clique_list}")

        return gkd_dict

    def babel_method(self):
        seen = {v : False for v in self.graph.nodes}
        for v in self.graph.nodes:
            gkd_dict = self.GKD()                   # Re-define the GKD model - meant to find the vertex with the maximum GKD that hasn't been seen after every iteration.   

            # Finding the vertices with the largest GKD  
            max_dict, max_len = {}, -1
            for key, val in gkd_dict.items():
                print(f"Here at {key} with a list of length {len(val)}")
                if len(val) > max_len and not seen[key]: 
                    max_dict, max_len = {}, len(val)
                    max_dict[key] = val
                elif len(val) == max_len: 
                    max_dict[key] = val

            # Breaking ties with the heaviest vertex in the graph
            max_list, max_vertex_weight, max_vertex = None, -1, -1
            for key, val in max_dict.items():
                if self.weights[key] > max_vertex_weight and not seen[key]: 
                    max_list = val
                    max_vertex = key
                    max_vertex_weight = self.weights[key]

            # Mark max_vertex as seen
            seen[max_vertex] = True                
            print(f"Vertex {max_vertex} was the optimal GKD - flagging as seen ...")

            for clique in max_list: print(f"Clique in Max List: {clique}")

            # Initializing W with the weight of max_vertex
            W_value = self.weights[max_vertex]

            print(f"Current Weight: {W_value}")

            # Check every clique in the current clique list 
            for clique in self.clique_list:
                Nv = list(nx.neighbors(self.graph, max_vertex))

                # If the clique is a subset of the neighborhood of max_vertex, decrement W_value and append max_vertex to the current clique
                if set(clique).issubset(Nv):                        
                    clique.append(max_vertex)
                    W_value -= 1
                if W_value == 0: break
            
            # Append singleton cliques of max_vertex W_value times
            if W_value > 0: 
                for _ in range(W_value): self.clique_list.append([max_vertex])

        # print(f"Final clique list: {self.clique_list}")

        # Check that the equivalent defintion of the weighted clique cover is satisfied. 
        for v in self.graph.nodes:
            # print(f"W({v}) = {self.weights[v]}")
            clique_count = 0
            for clique in self.clique_list:
                if v in clique: clique_count += 1
            if self.weights[v] <= clique_count: 
                print(f"Pass! We have |K : {v} in K| >= w({v})")
            else: print(f"Error! We have |K : {v} in K| < w({v}) ...")

        print("Final Clique List: ")
        for clique in self.clique_list:
            print(f"Clique {clique}")

    def node_elimination(self): 
        rsf_model = RSF()
        S_hat = rsf_model.find_simplicial(self.graph)
        S = rsf_model.indepSimplicial(self.graph, S_hat)

        # print(f"S_hat output: {S_hat}")
        # print(f"S output: {S}")

        K_mathcal = {}
        for v in self.graph.nodes:
            non_Nv = list(nx.non_neighbors(self.graph, v))
            non_Nv.append(v)
            K_mathcal[v] = [] 
            for u in non_Nv:
                for clique in self.clique_list:
                    if u in clique: K_mathcal[v].append(clique)

        S_weight = 0
        for v in S: S_weight += self.weights[v]
        self.S, self.S_weight = S, S_weight

        print(f"S Output: {S} - Weight: {S_weight}")

        for v in self.graph.nodes:
            clique_list = K_mathcal[v]
            if len(clique_list) <= S_weight:
                print(f"Here in if statement - Vertex {v} ...")

                non_Nv = list(nx.non_neighbors(self.graph, v))
                non_Nv.append(v)
                mwis_model = WMISIP(nx.induced_subgraph(self.graph, non_Nv), self.weights)
                mwis_model.optimize()
                G_alpha = mwis_model.opt_cost()

                if G_alpha <= S_weight: print("We hit this case!")
                else: print("Something else ...")

    def branching_scheme(self):
        # curr_cliques = list(nx.find_cliques(self.graph))
        # print(f"Cliques in G: {curr_cliques}")

        r = {}
        for v in self.graph.nodes:
            max_idx = 0
            for idx, clique in enumerate(self.clique_list):
                if v in clique: max_idx = idx
                r[v] = max_idx
            print(f"Vertex {v} - Max index = {max_idx}")

        v_order = []
        for entry in sorted(r.items(), key=lambda item: item[1]): v_order.append(entry[0])

        s_idx = len(v_order)-1
        for idx in range(len(v_order)):
            if v_order[idx] > self.S_weight:
                s_idx = idx

        print("Final output: ")
        for v in range(s_idx+1, len(v_order)-1): print(f"Vertex: {v}")