## Name: branch_strat.py
## Description: This program executes a branch and bound algorithm as created by Balas and Yu
##              via the algorithm stated in "Combinatorial Branch-and-Bound for the Maximum Weight
##              Combinatorial Branch-and-Bound for the Maximum Weight Independent Set Problem"
##              
##              See Section 3 / Subsection 3.1 - "Balas & Yu"

import sys
import networkx as nx
import matplotlib.pyplot as plt
from random import random

# Step 1: Generate an arbitrary graph G = (V,E) and independent set S \subset V
# Step 2: Find an independent set U \subset V such that \alpha(G(U)) \leq V
# Setp 3: Collect vertices in V \ U as x1, x2, ..., x_k
# Step 4: ...

class RandGraph:
    ## Name: __init__ (Driver)
    ## Description: Initializes the number of vertices and edges,
    ##              V and E, respectively, to the graph G = (V,E).
    ## Argument(s):
    ## * card_v: The number of vertices to G = (V,E)
    ## * card_e: The number of edges to G = (V,E)
    ## Return(s): None
    def __init__(self, card_v): self.card_v = card_v

    ## Name: generate_V
    ## Description: Generates the set of vertices, V, to the graph G = (V,E).
    ## Argument(s): None
    ## Return(s): The set of vertices, V, to G = (V,E)
    def generate_V(self):
        V = []                                                      ## Empty list of vertices to G = (V,E)
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
                add_edge = 1 if random() < 0.50 else 0              ## Randomly decide whether an edge is added
                if i < j and add_edge: E.append([i,j])
        
        return E

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

class RandIndSet:
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
        
    ## Name: gen_ind_set
    ## Description: Generates a random independent set U \subseteq S to G = (V,E).
    ## Argument(s): None
    ## Return(s): None
    def gen_ind_set(self):
        U = []                                                      ## Independent set U
       
        for v in self.V:
            invalid = False
            selected = 1 if random() < 0.5 else 0
            if selected:                                            ## Check if a vertex is selected
                for u in U:
                    if [u,v] in E: invalid = True                   ## Check if there's a connection to vertices in U
                if not invalid: U.append(v)
        
        return U
    
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
    
    IndSet = RandIndSet(V,E)
    S = IndSet.gen_ind_set()                                        ## Random independent set S
    
#    for s in S: print(s)                                           ## Display the generated independent set
    
    G_disp = GraphVisual(V,E)
    G_disp.display()
