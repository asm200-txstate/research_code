## Name: branch_strat.py
## Description: This program executes a branch and bound algorithm as created by Balas and Yu
##              via the algorithm stated in "Combinatorial Branch-and-Bound for the Maximum Weight
##              Combinatorial Branch-and-Bound for the Maximum Weight Independent Set Problem"
##              
##              See Section 3 / Subsection 3.1 - "Balas & Yu"

import sys
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from random import random
import gurobipy as gp
from gurobipy import GRB

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
    def __init__(self,V,E):
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
    
    ## Name: disp_ind_subgraph
    ## Description: Displays the induced subgraph, G[U] := (U,\tilde{E}), within the graph G=(V,E).
    ## Argument(s): None
    ## Return(s): None
    def disp_ind_subgraph(self,U,Et):
        G = nx.Graph()
        G.add_nodes_from(self.V)
        G.add_edges_from(self.E)
        
        pos = nx.circular_layout(G, 2)
        
        extras = {"node_size" : 800}                                ## Supplemental details to networkx
        
        nx.draw_networkx(G, pos, width=3, font_size=18, font_color='white', **extras)
        
        ## Node Updates
        nx.draw_networkx_nodes(G, pos, nodelist=U, node_color="tab:red", **extras)
        
        ## Edge Updates
        nx.draw_networkx_edges(G, pos, width=3, edgelist=Et, edge_color="tab:red", **extras)
        
        ## Formats the legend in plot
        legend_elements = [
            Line2D([0], [0], marker='o', label='G = (V, E)', markerfacecolor='tab:blue'),
            Line2D([0], [0], marker='o', label=r'$\tilde{G} = (U, \tilde{E})$', markerfacecolor='tab:red', color='tab:red')
        ]

        plt.legend(handles=legend_elements, loc='upper right')

        plt.title(r"Induced Subgraph Plot")
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
    ## Return(s): An independent set S \subseteq V
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
        
    ## Name: mis_cost
    ## Description: Uses an IP to determine the optimal cost to the maximum independent set a graph G = (U, \tilde{E})
    ## Argument(s):
    ## * U - Set of vertices to G = (U, \tilde{E})
    ## * Et - Set of edges to G = (U, \tilde{E})
    ## Return(s): The optimal cost to the maximal independent set problem to G = (U, \tilde{E})
    def mis_cost(self, U, Et):
    
        model = gp.Model("mis_model")
        model.setParam("OutputFlag", 0)                             ## Prevent all comments from spamming terminal
        
        x = model.addVars(U, vtype=GRB.BINARY, name="DV: x")
        
        ## Edge Constraints
        for [u,v] in Et:
            model.addConstr(x[u] + x[v] <= 1, f"C1 - Edge: ({u},{v})")
            
        ## Vertex Constraints
        for u in U:
            model.addConstr(x[u] >= 0, f"C2: {u}")

        cost_coeff = []
        for v in U:
            cost_coeff.append(1)                                    ## Unweighted maximum independent set
            
        c = {v : cost_coeff[i] for i, v in enumerate(U)}

        ## Objective Function: max c'x
        objective = gp.quicksum(c[v] * x[v] for v in U)
        model.setObjective(objective, gp.GRB.MAXIMIZE)
    
        ## Perform optimization
        model.optimize()
        
        ## Returning the optimal cost (max c'x)
        opt_cost = model.ObjVal
        
        return opt_cost
        
    ## Name: mis_set
    ## Description: Uses an IP to determine the maximum independent set to an induced subgraph, G[U], of G = (U,V)
    ## Argument(s):
    ## * U - Set of vertices to G = (U, \tilde{E})
    ## * Et - Set of edges to G = (U, \tilde{E})
    ## Return(s): The set solution to the maximal independent set problem to G = (U, \tilde{E})
    def mis_set(self, U, Et):
        model = gp.Model("mis_model")
        model.setParam("OutputFlag", 0)                             ## Prevent all comments from spamming terminal
        
        x = model.addVars(U, vtype=GRB.BINARY, name="DV: x")
        
        ## Edge Constraints
        for [u,v] in Et:
            model.addConstr(x[u] + x[v] <= 1, f"C1 - Edge: ({u},{v})")
            
        ## Vertex Constraints
        for u in U:
            model.addConstr(x[u] >= 0, f"C2: {u}")

        cost_coeff = []
        for v in U:
            cost_coeff.append(1)                                    ## Unweighted maximum independent set
            
        c = {v : cost_coeff[i] for i, v in enumerate(U)}

        ## Objective Function: max c'x
        objective = gp.quicksum(c[v] * x[v] for v in U)
        model.setObjective(objective, gp.GRB.MAXIMIZE)
    
        ## Perform optimization
        model.optimize()
        
        # Display optimal solution
        print("Optimal Solution: ")
        for v in model.getVars():
            print(f"{v.VarName}, {v.X:.0f}")
        
        Si = []
        for soln, v in zip(x, model.getVars()):
            if v.X == 1:
                Si.append(soln)
                print(f"soln: {soln}")
        
        return Si
        
    ## Name: gen_Vi
    ## Description: Generates the set Vi := \overline{N}(xi) \ {xj : j < i}
    ## Argument(s):
    ## * x - Renamed as VnU, the list of entires in V but not in U
    ## * i - Renamed as v, the ith vertex in VnU, used to construct Vi
    ## Return(s): The constructed set Vi in step 3
    def gen_Vi(self, x, i):
        Vi = []
    
        Ni = []                                                 ## Neighborhood of v
        for e in self.E:
            u1, u2 = e
            if x[i] in [u1, u2]:
                if x[i] != u1: Ni.append(u1)
                else: Ni.append(u2)
        
        print(f"x{i} = {x[i]} | N(x{i}):", Ni)
        
        ## Append vertices, generate \tilde{x} := {xj : j < i}
        xj_tilde = []
        for j in range(len(x)):
            if j < i: xj_tilde.append(x[j])
            
        print("xj_tilde:", xj_tilde)
        
        NotNi = []
        for u in self.V:                                        ## Non-neighborhood of v
            if (u not in Ni) and (u != x[i]): NotNi.append(u)
    
        print(f"NotNi(x{j}):", NotNi)
        
        Vi = NotNi                                              ## Vertex Vi set
        for v in xj_tilde:
            if v in NotNi: Vi.remove(v)
    
        print(f"V{i}:", Vi)
        
        return Vi
            
    ## Name: gen_Ei
    ## Description: Find the set of edges to a subset of vertices to V
    ## Argument(s):
    ## * U - A subset of vertices to the induced subgraph, G[U]
    ## Return(s):
    ## * Ei - Denoted as \tilde{E}, the set of all edges to the induced subgraph
    def gen_Ei(self, U):
        Ei = []
        
        for e in self.E:
            u, v = e
            if u in U and v in U:
                Ei.append(e)                                        ## Append if both endpoints of e are in U
        
        return Ei

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Invalid argument count: {len(sys.argv)} - Try again ...")
        exit()
    
    v_count = int(sys.argv[1])                                      ## Vertex Count
    if v_count < 0:                                                 ## Check for valid |V|
        print("Invaid vertex count, setting |V| = 1")
        v_count = 1
    
#    ## Generating a random graph G = (V,E)
#    G_rand = RandGraph(v_count)
#    V = G_rand.generate_V()
#    E = G_rand.generate_E()

    ## Create a specific graph (temporarily)
    V = [v+1 for v in range(10)]
    E = [[1,2], [2,3], [3,4], [4,5],
         [6,7], [7,8], [8,9], [9,10], [3,8]]
    
    G_disp = GraphVisual(V,E)
    
#    ## Generating a random independent set, S, of vertices to G = (V,E)
#    Rand_IS = RandIndSet(V,E)
#    S = Rand_IS.gen_ind_set()
    S = [1,3]
    
    ## Perform the Branch and Bound Strategy by Balas & Yu
    BB = BBStrat(V,E)
    
    ## Step 1: Find U \subseteq V where \alpha(G[U]) \leq |S|
    U = []
    valid = False                                                   ## Check if alpha(G[U]) <= |S|
    while not valid:
        ## Step 1a: Find a subset to V called U
        U = []                                                      ## Reset after each iteration
        for v in V:
            if random() < 0.5: U.append(v)                          ## Select some vertices
        
        ## Step 1b: Find the edges to the induced subgraph, G[U]
        Et = BB.gen_Ei(U)
        
        ## Step 1c: Find the maximal independent set to the induced subgraph of G[U] := (U, \tilde{E})
        a_Gu = BB.mis_cost(U, Et)
        
        ## Step 1d: Check if alpha(G[U]) <= |S|
        if a_Gu <= len(S): valid = True
#    U = [4,5,8,9]
    Et = BB.gen_Ei(U)
    
    print("U: ", U)
    
    G_disp.disp_ind_subgraph(U, Et)
    exit()
    
    ## Step 2: Order vertices of V\U as x_{1}, ..., x_{k}
    VnU, idx = [], 0
    for v in V:
        if v not in U:
            VnU.append(v)
            idx += 1
        
    ## Step 3: For each i, let Vi := \overline{N}(xi) \ {xj : j < i}
    ## and find a maximal independent set Si in G[Vi]
    
    print("\nVnU:", VnU, "\n")
    
    S_list = []
    S_list.append(S)                                                 ## Append the first independent set
    
    idx = 0
    for i in range(len(VnU)):
        Vi = BB.gen_Vi(VnU,i)
        Ei = BB.gen_Ei(Vi)
        
        Si = BB.mis_set(Vi,Ei)
        Si.append(VnU[i])
        Si.sort()
        
        S_list.append(Si)
        
#        G_disp.disp_ind_subgraph(Vi,Ei)
        
        idx += 1
        
    ## Determine which is the largest maximal independent subset
    
    S_final = []
    for Si in S_list:
        if len(Si) > len(S_final): S_final = Si
    
    print("Final output: ", S_final)
