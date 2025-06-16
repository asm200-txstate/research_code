import gurobipy as gp
from gurobipy import GRB, quicksum

import networkx as nx

class CCIP:
    def __init__(self, G, cliques):
        self.G = G
        self.cliques = cliques

        self.model = gp.Model("mcc_model")
        self.model.setParam("OutputFlag", 0)                            ## Prevent all comments from spamming terminal

        self.clique_cover = []

    def optimize(self):
        ## Define decision variables
        x = self.model.addVars(range(len(self.cliques)), lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="DV: x")

        ## Clique constraint - \Sum cliques that vertex i appears for i \in G.nodes() such that \Sum >= 1
        for v in self.G.nodes():
            self.model.addConstr(
            gp.quicksum(x[u] for u, clique in enumerate(self.cliques) if v in list(clique)) >= 1, 
                name=f"cover_{v}"
            )
        
        cost = [1 for _ in range(len(self.cliques))]
        
        ## Objective Function: max c'x
        objective = gp.quicksum(cost[v] * x[v] for v in range(len(self.cliques)))
        self.model.setObjective(objective, gp.GRB.MINIMIZE)

        ## Perform optimization
        self.model.optimize()

        ## Find the solution
        for soln, v in zip(x, self.model.getVars()):
            if v.X == 1: self.clique_cover.append(self.cliques[soln])

    def opt_cost(self):
        return self.model.ObjVal

    def opt_soln(self):
        return self.clique_cover
