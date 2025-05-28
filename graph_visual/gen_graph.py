# Name: gen_visual.py
# Description: Generate a randomized graph that's an induced subgraph to a complete
#              graph G = (V,E). The following graph is displayed to the graph. 

import sys
import networkx as nx
import matplotlib.pyplot as plt
import gurobipy as gp
import gurobipy as GRB
from random import randint

class GraphVisual:
    ## Name: __init__ (Driver)
    ## Description: Initializes the set of vertices and edges, denoted
    ##              V and E, respectively, for the graph G = (V,E).
    ## Argument(s):
    ## * V: Set of vertices to G.
    ## * E: Set of edges to G.
    def __init__(self, V, E):
        self.V = V
        self.E = E

    ## Name: display_graph
    ## Description: Displays the randomized graph to the terminal.
    ## Argument(s): None
    def display(self):
        pass
    
class RandGraph:
    ## Name: __init__ (Driver)
    ## Description: Initializes the number of vertices and edges,
    ##              V and E, respectively, to the graph G = (V,E).
    ## Argument(s):
    ## * card_v: The number of vertices to G = (V,E)
    ## * card_e: The number of edges to G = (V,E)
    def __init__(self, card_v, card_e):
        self.card_v = card_v
        self.card_e = card_e

    ## Name: generate_V
    ## Description: Generates the set of vertices, V, to the graph G = (V,E).
    ## Argument(s): None
    def generate_V(self):
        V = []                                              # Empty list of vertices to G = (V,E)
        for v in range(self.card_v): V.append(f"v{v}")
        return V
            
    ## Name: generate_E
    ## Description: Generates the set of edges, E, to the graph G = (V,E).
    ## Argument(s): None
    def generate_E(self):
        pass
        
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Invalid argument count: {len(sys.argv)} - Try again ...")
        exit()
    
    v_count = int(sys.argv[1])                      ## Vertex Count
    e_count = int(sys.argv[2])                      ## Edge Count
    
    if v_count < 0:                                 ## Check for valid |V|
        print("Invaid vertex count, setting |V| = 1")
        v_count = 1
    
    max_simple = (v_count * (v_count - 1)) // 2     ## Check for valid |E| / max_simple := C(|V|,2)
    if e_count > max_simple:
        print(f"Invalid edge count, setting |E| = {max_simple}")
        e_count = max_simple
    
    ## Generating a random graph
    G_rand = RandGraph(v_count, e_count)
