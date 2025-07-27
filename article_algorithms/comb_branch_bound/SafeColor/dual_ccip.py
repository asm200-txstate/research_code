import networkx as nx

import gurobipy as gp
from gurobipy import GRB, quicksum

class dual_ccip:
    def __init__(self, G : nx, cliques : list): 
        self.graph = G
        self.cliques = cliques

        self.model = gp.Model("dual_cc_model")
        self.model.setParam("OutputFlag", 0)                            ## Prevent all comments from spamming terminal

        self.output_y = []
        self.output_z = []

        self.cost_y = []
        self.cost_z = []
    
    def optimize(self): 

        # # Get variable values
        # for v in self.graph.nodes:
        #     print(f"y[{v}] = {y[v].X}")

        # for s_idx in range(len(self.cliques)):
        #     print(f"z[{s_idx}] = {z[s_idx].X}")

        # Dual variables
        y_node = self.model.addVars(self.graph.nodes, lb=0.0, vtype=GRB.CONTINUOUS, name="DV: y")               # y_v >= 0
        z_clique = self.model.addVars(range(len(self.cliques)), lb=0.0, vtype=GRB.CONTINUOUS, name="DV: z")     # z_S >= 0

        # Constraints: sum_{v in S} y_v - z_S <= 1 for all S
        for idx, clique in enumerate(self.cliques):
            self.model.addConstr(gp.quicksum(y_node[v] for v in clique) - z_clique[idx] <= 1)
        
        ## Objective Function: maximize sum(y_v) - sum(z_S)
        self.model.setObjective(
            gp.quicksum(y_node[u] for u in self.graph.nodes)- 
            gp.quicksum(z_clique[v] for v in range(len(self.cliques))), 
            gp.GRB.MAXIMIZE
        )

        ## Perform optimization
        self.model.optimize()

        print(f"y_node: {y_node}")
        for v in y_node: 
            print(f"Node {v}: y = {y_node[v].X}")
        for k in z_clique: print(f"Clique {k}: z = {z_clique[k].X} - Clique {self.cliques[k]}")

        ## Find the solution to y_node
        for soln, v in zip(y_node, self.model.getVars()):
            self.cost_y.append(v.X)
            if v.X > 0: 
                self.output_y.append(soln)
                # print(f"Y: {soln} - v: {v.X}")

        ## Find the solution to z_clique
        for soln, v in zip(z_clique, self.model.getVars()):
            self.cost_z.append(v.X)
            if v.X > 0: 
                self.output_z.append(self.cliques[soln])
                # print(f"Z: {self.cliques[soln]} - v: {v.X}")

    def opt_cost(self): return self.model.ObjVal, self.cost_y, self.cost_z

    def opt_soln(self): return self.output_y, self.output_z