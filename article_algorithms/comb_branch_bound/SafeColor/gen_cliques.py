import sys
sys.setrecursionlimit(1000000)                                                  # Recursion level limit - 1,000,000 levels

import networkx as nx

class gen_cliques:
    def __init__(self, G : nx):
        self.graph = G

    def find_mis(self, mis_set : set, curr_nodes : list, start_node : int):
        if start_node >= len(self.graph):                                        # All nodes in G have been seen
            try: 
                curr_list = list(nx.maximal_independent_set(self.graph, curr_nodes))     # Check if curr_nodes list is an stable set
                mis_set.add(frozenset(curr_list))
            except: pass                                                        # Invalid set - not a stable set. Continue moving forward. 
            return

        # Iterate through every vertex in G (starting from start_node)
        for v in list(self.graph)[start_node:]:
            if v in curr_nodes: continue
            curr_nodes.append(v)
            self.find_mis(mis_set, curr_nodes, start_node + 1)
            curr_nodes.remove(v)

        # Make recursive calls without appending start_node
        self.find_mis(mis_set, curr_nodes, start_node + 1)
