# Name: gen_visual.py
# Description: Generate a randomized graph that's an induced subgraph to a complete
#              graph G = (V,E). The following graph is displayed to the graph. 

import sys
import networkx as nx
import matplotlib.pyplot as plt
from random import randint

class GraphVisual:
    ## Name: __init__ (Driver)
    ## Description: Initializes the set of vertices and edges, denoted
    ##              V and E, respectively, for the graph G = (V,E).
    ## Argument(s):
    ## * V: Set of vertices to G.
    ## * E: Set of edges to G.
    ## Return(s): None
    def __init__(self, V, E):
        self.V = V
        self.E = E

    ## Name: display_graph
    ## Description: Displays the randomized graph to the terminal.
    ## Argument(s): None
    ## Return(s): None
    def display(self):
        G = nx.Graph()
        G.add_nodes_from(self.V)
        G.add_edges_from(self.E)
        
        pos = nx.circular_layout(G, 2)
        
        nx.draw_networkx(G, pos)
        plt.title(f"Induced Subgraph for $K_{{{len(self.V)}}}$")
        plt.show()
    
class RandGraph:
    ## Name: __init__ (Driver)
    ## Description: Initializes the number of vertices and edges,
    ##              V and E, respectively, to the graph G = (V,E).
    ## Argument(s):
    ## * card_v: The number of vertices to G = (V,E)
    ## Return(s): None
    def __init__(self, card_v):
        self.card_v = card_v
        
    ## Name: generate_V
    ## Description: Generates the set of vertices, V, to the graph G = (V,E).
    ## Argument(s): None
    ## Return(s): None
    def generate_V(self):
        V = []                                              ## Empty list of vertices to G = (V,E)
        for v in range(self.card_v): V.append(v)
        return V
            
    ## Name: generate_E
    ## Description: Generates the set of edges, E, to the graph G = (V,E).
    ## Argument(s): None
    ## Return(s): The set of edges, E, to G = (V,E)
    def generate_E(self):
        E = []                                                      ## Empty list of edges to G = (V,E)
        
        for i in range(self.card_v):                                ## Generate edges to K_{card_v}
            for j in range(self.card_v):
                add_edge = randint(0,1)                             ## Randomly decide whether an edge is added
                if i < j and add_edge: E.append([i,j])
        
        return E

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Invalid argument count: {len(sys.argv)} - Try again ...")
        exit()
    
    v_count = int(sys.argv[1])                                      ## Vertex Count
    if v_count < 0:                                                 ## Check for valid |V|
        print("Invaid vertex count, setting |V| = 1")
        v_count = 1
    
    ## Generating a random graph
    G_rand = RandGraph(v_count)
    V = G_rand.generate_V()
    E = G_rand.generate_E()
    
    G_disp = GraphVisual(V,E)
    G_disp.display()
