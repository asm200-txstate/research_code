## ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** 
## Filename: main.py   
## 
## Author: Axel Sanchez Moreno
##
## Description: Text goes here ...
##
##
## Dependencies: 
##
## 
##
## 
##
##
##
##
## ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** 

import Graph.Graph as Graph
import gurobipy as gp
from gurobipy import GRB, quicksum

class MISIP:
    def __init__(self, G : Graph):
        self.Graph = G
        self.model = gp.Model("mis_model")
        self.model.setParam("OutputFlag", 0)                            ## Prevent all comments from spamming terminal
        self.set_soln = []

    def optimize(self):
        V, E = self.Graph.get_all_v(), self.Graph.get_all_e()

        ## Define decision variables
        x = self.model.addVars(V, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="DV: x") # Use GRB.BINARY, if needed

        ## Define edge constratins
        for [u, v] in E: self.model.addConstr(x[u] + x[v] <= 1, f"C1: ({u},{v})")
            
        ## Vertex Constraints
        for u in V: self.model.addConstr(x[u] >= 0, f"C2: {u}")

        cost = []
        for v in V: cost.append(1)                                      ## Unweighted maximum independent set
        
        c = {v : cost[i] for i, v in enumerate(V)}

        ## Objective Function: max c'x
        objective = gp.quicksum(c[v] * x[v] for v in V)
        self.model.setObjective(objective, gp.GRB.MAXIMIZE)
    
        ## Perform optimization
        self.model.optimize()

        ## Find the solution
        for soln, v in zip(x, self.model.getVars()):
            if v.X == 1: self.set_soln.append(soln)

    def opt_cost(self):
        return self.model.ObjVal

    def opt_soln(self):
        return self.set_soln 
