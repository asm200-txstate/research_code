import sys
import random
import networkx as nx

from BalasXue.WMISIP import WMISIP
from BalasYu.RecSimpFix import RSF

class BWCCMethod:
    def __init__(self, G : nx, W : dict): 
        self.graph = G
        self.weights = W
        self.clique_list, self.seen_list = [], []
        self.clique_list = list(nx.find_cliques(self.graph))
    
    def compute_GKD(self):
        # self.clique_list = list(nx.find_cliques(self.graph))
        gkd_vertex, gkd_weight = -1, -1
        for v in self.graph.nodes:
            clique_count = 0
            for u in nx.non_neighbors(self.graph, v):
                for C in self.clique_list:
                    if u in C: clique_count = clique_count + 1
            if gkd_weight < clique_count and v not in self.seen_list:
                gkd_vertex, gkd_weight = v, clique_count 

        self.seen_list.append(gkd_vertex)
        return gkd_vertex
    
    def is_adjacent(self, v : int, S : list):
        # print(f"Current list S: {S}")
        for u in S:
            if (u,v) in self.graph.edges:
                return True
        return False

    # Find the maximal independnet set from mis_cand_list    
    def mis_status(self, mis_cand_list : list):
        for jdx, curr_list in enumerate(mis_cand_list):
            G = self.graph.copy()
            for u in curr_list: 
                neighbors = list(nx.neighbors(G, u))
                G.remove_nodes_from(list(set(neighbors).union({u})))
            if list(G.nodes) == []: return jdx
        # print("")
        return -1
    
    def babel_scheme(self):
        final_idx, maximal_found, S = -1, False, []
        mis_cand_list, result_idx = [], -1


        for jdx in range(len(self.graph.nodes)):
            gkd_v = self.compute_GKD()
            W = self.weights[gkd_v]

            # print(f"Vertex: {gkd_v}")
            # print(f"GKD Candidate: {gkd_v} | Initial W: {W}")

            # Sort cliques from self.clique_list (review techniques later)
            t = len(self.clique_list)
            for idx in range(t):
                if set(self.clique_list[idx]).issubset(list(nx.neighbors(self.graph, gkd_v))): 
                    # print("Decrementing W ....")
                    self.clique_list[idx].append(gkd_v)
                    W = W - 1
                    if W == 0: break

            while W > 0: 
                # print(f"Current W: {W}")
                self.clique_list.append([gkd_v])
                matches = [sublist for sublist in self.clique_list if gkd_v in sublist]
                # print(f"Clique count containing {gkd_v}: ", len(matches))
                W = W - 1

            # print("")

            # Append the gkd_v vertex to every clique_list to update all independent sets - purpose: find a maximal independent set int he end. 
            for curr_list in mis_cand_list:
                if not maximal_found and not self.is_adjacent(gkd_v, curr_list): curr_list.append(gkd_v)
            mis_cand_list.append([gkd_v])

            if result_idx == -1: 
                result_idx = self.mis_status(mis_cand_list)
                # if result_idx != -1: print("Maximal independent set found!\n")
                # if result_idx != -1: print(f"Great news! Found it! - Index: {result_idx}\n")
                final_idx = result_idx
            
        S = mis_cand_list[result_idx]

        # print("")
    
        V = list(self.graph.nodes)
        for v in V:
            temp_list = []
            clique_count = 0
            for C in self.clique_list: 
                if v in C: 
                    clique_count = clique_count + 1
                    temp_list.append(C)
            if clique_count < self.weights[v]: 
                print("Invalid output ...")
            else: pass

        # Set of indices where for every v in V, r(v) = {j in [t] : v in Kj}
        rank = {}
        for v in self.graph.nodes:
            max_idx = -1
            for jdx, clique in enumerate(self.clique_list):
                if v in clique: max_idx = jdx
            rank[v] = max_idx
        
        # Sorting the vertices in V by their rank. 
        V_tilde, V_dict = [], {} 

        # Step 1: Map the vertices to their respective ranks.
        for v in self.graph.nodes:
            for idx, K in enumerate(self.clique_list): 
                if v in K: V_dict[v] = idx

        # Step 2: Use the lambda function to create the 
        #         final set, V_tilde such that r(v_s) > w(S)
        V_tilde = [k for k, v in sorted(V_dict.items(), key=lambda item: item[1], reverse=True)]
        
        weight_S = 0
        for v in S: 
            weight_S = weight_S + self.weights[v]

        # Make it to where you're using S instead of U.
        print(f"w(S) = {weight_S}")
        rank_weight_idx = -1 # List of indices such that rank[v] > W(s)
        for idx, s in enumerate(V_tilde):
            # print(f"Rank[{s}]: {rank[s]} - Index: {idx}")
            if rank[s] > weight_S: 
                # print(f"Rank[{s}]: {rank[s]} - Index: {idx}")
                rank_weight_idx = idx

        print(f"\nV_tilde Set: {V_tilde}")
        print(f"Candidate Max Index List: {rank_weight_idx}\n")

        v_s = rank_weight_idx # Save the largest index such that rank[s] > weight_S.
        print(f"Final Index Output (s): {v_s} - (Vertex, Rank) ({V_tilde[v_s]}, {rank[v_s]})") 
        
        U = V_tilde[v_s + 1 : len(V_tilde)]
        print(f"U set (V_tilde from s+1 to n): {U}")

        isgraph = nx.induced_subgraph(self.graph, U)
        mis_model = WMISIP(isgraph, self.weights)
        mis_model.optimize()
        cost_output = mis_model.opt_cost()

        print(f"\nalpha_w(G[U]): {cost_output}| w(S): {weight_S}")
        if cost_output <= weight_S: print("Valid output")
        else: print("Invalid output") 

        return

    # def babel_method(self):
    #     seen = {v : False for v in self.graph.nodes}
    #     for v in self.graph.nodes:
    #         gkd_dict = self.GKD()                   # Re-define the GKD model - meant to find the vertex with the maximum GKD that hasn't been seen after every iteration.   

    #         # Finding the vertices with the largest GKD  
    #         max_dict, max_len = {}, -1
    #         for key, val in gkd_dict.items():
    #             print(f"Here at {key} with a list of length {len(val)}")
    #             if len(val) > max_len and not seen[key]: 
    #                 max_dict, max_len = {}, len(val)
    #                 max_dict[key] = val
    #             elif len(val) == max_len: 
    #                 max_dict[key] = val

    #         # Breaking ties with the heaviest vertex in the graph
    #         max_list, max_vertex_weight, max_vertex = None, -1, -1
    #         for key, val in max_dict.items():
    #             if self.weights[key] > max_vertex_weight and not seen[key]: 
    #                 max_list = val
    #                 max_vertex = key
    #                 max_vertex_weight = self.weights[key]

    #         # Mark max_vertex as seen
    #         seen[max_vertex] = True                
    #         print(f"Vertex {max_vertex} was the optimal GKD - flagging as seen ...")

    #         for clique in max_list: print(f"Clique in Max List: {clique}")

    #         # Initializing W with the weight of max_vertex
    #         W_value = self.weights[max_vertex]

    #         print(f"Current Weight: {W_value}")

    #         # Check every clique in the current clique list 
    #         for clique in self.clique_list:
    #             Nv = list(nx.neighbors(self.graph, max_vertex))

    #             # If the clique is a subset of the neighborhood of max_vertex, decrement W_value and append max_vertex to the current clique
    #             if set(clique).issubset(Nv):                        
    #                 clique.append(max_vertex)
    #                 W_value -= 1
    #             if W_value == 0: break
            
    #         # Append singleton cliques of max_vertex W_value times
    #         if W_value > 0: 
    #             for _ in range(W_value): self.clique_list.append([max_vertex])

    #     # print(f"Final clique list: {self.clique_list}")

    #     # Check that the equivalent defintion of the weighted clique cover is satisfied. 
    #     for v in self.graph.nodes:
    #         # print(f"W({v}) = {self.weights[v]}")
    #         clique_count = 0
    #         for clique in self.clique_list:
    #             if v in clique: clique_count += 1
    #         if self.weights[v] <= clique_count: 
    #             print(f"Pass! We have |K : {v} in K| >= w({v})")
    #         else: print(f"Error! We have |K : {v} in K| < w({v}) ...")

    #     print("Final Clique List: ")
    #     for clique in self.clique_list:
    #         print(f"Clique {clique}")

    # def node_elimination(self): 
    #     rsf_model = RSF()
    #     S_hat = rsf_model.find_simplicial(self.graph)
    #     S = rsf_model.indepSimplicial(self.graph, S_hat)

    #     # print(f"S_hat output: {S_hat}")
    #     # print(f"S output: {S}")

    #     K_mathcal = {}
    #     for v in self.graph.nodes:
    #         non_Nv = list(nx.non_neighbors(self.graph, v))
    #         non_Nv.append(v)
    #         K_mathcal[v] = [] 
    #         for u in non_Nv:
    #             for clique in self.clique_list:
    #                 if u in clique: K_mathcal[v].append(clique)

    #     S_weight = 0
    #     for v in S: S_weight += self.weights[v]
    #     self.S, self.S_weight = S, S_weight

    #     print(f"S Output: {S} - Weight: {S_weight}")

    #     for v in self.graph.nodes:
    #         clique_list = K_mathcal[v]
    #         if len(clique_list) <= S_weight:
    #             print(f"Here in if statement - Vertex {v} ...")

    #             non_Nv = list(nx.non_neighbors(self.graph, v))
    #             non_Nv.append(v)
    #             mwis_model = WMISIP(nx.induced_subgraph(self.graph, non_Nv), self.weights)
    #             mwis_model.optimize()
    #             G_alpha = mwis_model.opt_cost()

    #             if G_alpha <= S_weight: print("We hit this case!")
    #             else: print("Something else ...")

    # def branching_scheme(self):
    #     # curr_cliques = list(nx.find_cliques(self.graph))
    #     # print(f"Cliques in G: {curr_cliques}")

    #     r = {}
    #     for v in self.graph.nodes:
    #         max_idx = 0
    #         for idx, clique in enumerate(self.clique_list):
    #             if v in clique: max_idx = idx
    #             r[v] = max_idx
    #         print(f"Vertex {v} - Max index = {max_idx}")

    #     v_order = []
    #     for entry in sorted(r.items(), key=lambda item: item[1]): v_order.append(entry[0])

    #     s_idx = len(v_order)-1
    #     for idx in range(len(v_order)):
    #         if v_order[idx] > self.S_weight:
    #             s_idx = idx

    #     print("Final output: ")
    #     for v in range(s_idx+1, len(v_order)-1): print(f"Vertex: {v}")