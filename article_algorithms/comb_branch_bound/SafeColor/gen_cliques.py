import sys
sys.setrecursionlimit(1000000)

def find_mis(G, mis_set, curr_nodes, start_node):

    if start_node >= len(G.nodes()):    # All nodes in G have been seen
        try: 
            curr_list = list(nx.maximal_independent_set(G, curr_nodes))    # Check if curr_nodes list is an stable set
            mis_set.add(frozenset(curr_list))
        except: pass                                                        # Invalid set - not a stable set. Continue moving forward. 
        return

    # Iterate through every vertex in G (starting from start_node)
    for v in list(G.nodes())[start_node:]:
        if v in curr_nodes: continue
        curr_nodes.append(v)
        find_mis(G, mis_set, curr_nodes, start_node + 1)
        curr_nodes.remove(v)

    # Make recursive calls without appending start_node
    find_mis(G, mis_set, curr_nodes, start_node + 1)

class gen_cliques:
    def __init__(self):
        pass