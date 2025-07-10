import sys
import random
import networkx as nx

from BalasXue.WMISIP import WMISIP

class BMethod:
    def __init__(self, G : nx, W : dict): 
        self.graph = G
        self.weights = W
        self.clique_list = []

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

        # for key, cliques in gkd_dict.items():
        #     print(f"Key: {key} - Clique(s): {list(cliques)}")

        return gkd_dict
    
    ## Note: Temporary, check with Dr. Hicks on the remark made in Page 7 - Potential 
    ## bug (or misunderstood step) in implementing the Babel Method (Part 1 method)
    def maximal_is(self):
        V, S = list(self.graph.nodes), []
        while V != []:
            v = random.choice(V)
            S.append(v)
            V.remove(v)
            for u in nx.neighbors(self.graph, v): 
                if u in V: V.remove(u)
        return S

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
        S = self.maximal_is()
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
        pass