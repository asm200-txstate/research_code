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
        
    def optimize(self, S):
        V, E = self.Graph.get_all_v(), self.Graph.get_all_e()

        ## Define decision variables
        x = self.model.addVars(V, lb=0.0, ub=1.0, vtype=GRB.CONTINUOUS, name="DV: x") # Use GRB.BINARY, if needed

        ## Define edge constratins
        for [u, v] in E: self.model.addConstr(x[u] + x[v] <= 1, f"C1: ({u},{v})")
            
        ## Vertex Constraints
        for u in V: self.model.addConstr(x[u] >= 0, f"C2: {u}")

        ## Cardinality constraint (\alpha(G[U]) <= |S|)
        self.model.addConstr(quicksum(x[v] for v in V) <= len(S), "C3: |S|")

        cost = []
        for v in V: cost.append(1)                                    ## Unweighted maximum independent set
        
        c = {v : cost[i] for i, v in enumerate(V)}

        ## Objective Function: max c'x
        objective = gp.quicksum(c[v] * x[v] for v in V)
        self.model.setObjective(objective, gp.GRB.MAXIMIZE)
    
        ## Perform optimization
        self.model.optimize()

        ## Find the solution here ...
    
    def opt_cost(self):
        return self.model.ObjVal

    def opt_soln(self):
        pass
    
        # # Display optimal solution
        # print("Optimal Solution: ")
        # for v in self.model.getVars():
        #     print(f"{v.VarName}, {v.X:.0f}")
        
        # Si = []
        # for soln, v in zip(x, self.model.getVars()):
        #     if v.X == 1:
        #         Si.append(soln)
        #         print(f"soln: {soln}")
        
        # # return Si