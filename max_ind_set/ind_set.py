import numpy as np
import gurobipy as gp
from gurobipy import GRB

if __name__ == "__main__":
    print("Here in main")
    
    # Defining graph G = (V, E)
    V = [1,2,3,4,5]
    E = [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4],[3,5],[4,5]]
    
    # Creating model
    model = gp.Model("mis_model") # Max Independent Set Model
    
    # Defining decision variable x \in {0,1}^{V}
    x = model.addVars(V, vtype=GRB.BINARY, name="DV: x")
    
    # Constraint: x_{u} + x{v} <= 1 for all uv \in E
    # Description: Ensure no more than one vertex is counted
    for [u,v] in E:
        model.addConstr(x[u] + x[v] <= 1, f"C1 - Edge: ({u},{v})")
    
    # Constraint: x_{u} >= 0 for all u \in V
    # Description: Ensure all vertices are non-negative
    for v in V:
        model.addConstr(x[v] >= 0, f"C2: {v}")

    # Defining cost coefficient dictionary
    # Description: Setting all vertex weights as equal
    cost_coeff = [1, 1, 1, 1, 1]
    c = {v : cost_coeff[i] for i, v in enumerate(V)}
    
    # Objective Function: max c'x
    objective = gp.quicksum(c[v] * x[v] for v in V)
    model.setObjective(objective, gp.GRB.MAXIMIZE)
    
    # Perform optimization
    model.optimize()
    
    # Display optimal solution
    print("Optimal Solution: ")
    for v in model.getVars():
        print(f"{v.VarName}, {v.X:.0f}")
    
    # Display optimal cost
    print("Optimal Cost: ")
