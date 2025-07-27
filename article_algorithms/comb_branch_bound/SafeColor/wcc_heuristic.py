import numpy as np
import networkx as nx

class wcc_generator:
    def __init__(self, G : nx, W_dict : dict, S_dict : dict):
        self.graph = G
        self.weight_dict = W_dict
        self.seen_dict = S_dict

        self.cliques = []
        self.clique_weights = []

    def min_node_unseen(self, pi_prime):
        min_node = -1
        min_val = 2**63 - 1 
        for v in pi_prime.keys():
            if self.seen_dict[v] == False: 
                if min_val >= pi_prime[v]:  min_node, min_val = v, pi_prime[v]
        return min_node

    def max_val_clique(self, clique):
        max_val = -2**63 
        for v in clique:
            if max_val < self.weight_dict[v]:
                max_val = self.weight_dict[v]
        return max_val

    def wwc_heuristic(self): 
        pi_prime = self.weight_dict.copy()

        while True:
            v = self.min_node_unseen(pi_prime) # min(pi_prime, key=pi_prime.get)
            N_v = list(nx.neighbors(self.graph, v))
            # Nv_update = [v for v in N_v if self.seen_dict[v] == False]

            Nv_update = []
            for u in N_v:
                print(f"Node {u}, Status: {self.seen_dict[u]}")
                if self.seen_dict[u] == False:
                    Nv_update.append(u)
            print(f"Final Nv_update: {Nv_update}")

            clique = []
            for u in Nv_update:
                cliques = list(nx.find_cliques(self.graph, [u]))
                for C in cliques:
                    print(f"*** C: {C} | Nv_update: {Nv_update} = {set(C).issubset(Nv_update)}")
                    if set(C).issubset(Nv_update): clique = C

            clique.append(v)
            max_weight_val = self.max_val_clique(clique)
            self.cliques.append(clique.copy())
            self.clique_weights.append(max_weight_val)
            clique.remove(v)

            for u in clique: self.weight_dict[u] = self.weight_dict[u] - self.weight_dict[v]
            
            self.weight_dict[v] = 0
            self.seen_dict[v] = True
            
            all_seen = True
            for status in self.seen_dict.values():
                if status == False: 
                    all_seen = False
                    break

            seen_status = all(not value for value in self.seen_dict.values())
            print(f"Status: {self.seen_dict.values()}")
            print(f"Overall: {all_seen}\n")
            if all_seen == True: break
            
    def weighted_cliques(self): 
        print(f"Cliques: {self.cliques}")
        pass
