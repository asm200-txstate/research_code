import gurobipy as gp
from gurobipy import GRB, quicksum

class WMISIP:
    def __init__(self, G, W):
        self.graph = G
        self.weights = W

        self.soln = []
        self.cost = 0

        self.model = gp.Model("wmis_model")
        self.model.setParam("OutputFlag", 0)                            ## Prevent all comments from spamming terminal

    def optimize(self):
        V, E = self.graph.nodes, self.graph.edges

        ## Define decision variables
        x = self.model.addVars(V, lb=0.0, ub=1.0, vtype=GRB.BINARY, name="DV: x")

        ## Define edge constratins
        for [u, v] in E: self.model.addConstr(x[u] + x[v] <= 1, f"C1: ({u},{v})")

        ## Objective Function: max c'x
        objective = gp.quicksum(self.weights[v] * x[v] for v in V)                                 ## Weighted maximum independent set
        self.model.setObjective(objective, gp.GRB.MAXIMIZE)

        ## Perform optimization
        self.model.optimize()

        ## Find the solution
        for soln, v in zip(x, self.model.getVars()):
            if v.X == 1: 
                self.soln.append(soln)
                self.cost = self.cost + self.weights[soln]
                
    def opt_cost(self): return self.cost

    def opt_soln(self): return self.soln