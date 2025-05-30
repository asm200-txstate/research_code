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
        
        nx.draw_networkx(G, pos, width=2, node_size=800, font_size=12, font_color='white')
        plt.title(f"Induced Subgraph for $K_{{{len(self.V)}}}$")
        plt.show()

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
        S = []                                                      ## Independent set S
        
        for v in self.V:
            invalid = False
            selected = 1 if random() < 0.5 else 0
            if selected:                                            ## Check if a vertex is selected
                for s in S:
                    if [s,v] in E: invalid = True                   ## Checks if the vertex has edges that aren't included to the pre-constructed set, U
                if not invalid: S.append(v)
        
        return S                                                    ## Return the final result
        
class BBStrat:
    ## Name: __init__ (driver)
    ## Description: Initializes the graph G = (V,E)
    ## Argument(s):
    ## * V - The set of vertices to the graph G = (V, E)
    ## * E - The set of edges to the grpah G = (V, E)
    ## Return(s): None
    def __init__(self, V, E):
        self.V = V
        self.E = E
    
    ## Name: find_ind_set
    ## Description: Find an independent set U \subseteq V such that \alpha(G[U]) <= |S|
    ## Argument(s):
    ## * U - A subset of vertices to the induced subgraph, G[U]
    ## Return(s):
    ## * Et - Denoted as \tilde{E}, the set of all edges to the induced subgraph
    def edge_set(self, U):
        Et = []
        
        for e in self.E:
            u, v = e
            if u in U and v in U:
                Et.append(e)                                        ## Append if both endpoints of e are in U
        
        return Et
    
    ## Name: max_ind_set
    ## Description: Uses an IP to determine the maximum independent set to an induced subgraph, G[U], of G = (U,V)
    ## Argument(s): None
    ## Return(s): None
    def gen_max_ind_set(self, U, Et):
        pass
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Invalid argument count: {len(sys.argv)} - Try again ...")
        exit()
    
    v_count = int(sys.argv[1])                                      ## Vertex Count
    if v_count < 0:                                                 ## Check for valid |V|
        print("Invaid vertex count, setting |V| = 1")
        v_count = 1
    
    ## Generating a random graph G = (V,E)
    G_rand = RandGraph(v_count)
    V = G_rand.generate_V()
    E = G_rand.generate_E()
    
    ## Generating a random independent set of vertices to G = (V,E)
    Rand_IS = RandIndSet(V,E)
    S = Rand_IS.gen_ind_set()                                       ## Generating a random independent set S

#    IndSet.find_ind_set()                                          ## Finds an independent set U \subseteq V where \alpha(G[U]) <= |S|
    
#    for s in S: print(s)                                            ## Display the generated independent set
            
    ## Perform the Branch and Bound Strategy by Balas & Yu
    BB = BBStrat(V,E)
    
    ## Step 1a: Find a subset to V called U
    U = []
    for v in V:
        if random() < 0.5: U.append(v)                              ## Select some vertices
    
    ## Step 1b: Find the edges to the induced subgraph, G[U]
    Et = BB.edge_set(U)
    
    ## Step 1c: Find the maximal independent set to the induced subgraph of G[U] := (U, \tilde{E})
    a_Gu = BB.gen_max_ind_set(U,Et)
    
    
    
    
    G_disp = GraphVisual(V,E)
    G_disp.display()
