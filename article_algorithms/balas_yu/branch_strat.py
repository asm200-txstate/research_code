## Name: branch_strat.py
## Description: This program executes a branch and bound algorithm as created by Balas and Yu
##              via the algorithm stated in "Combinatorial Branch-and-Bound for the Maximum Weight
##              Combinatorial Branch-and-Bound for the Maximum Weight Independent Set Problem"
##              
##              See Section 3 / Subsection 3.1 - "Balas & Yu"

# Step 1: Generate an arbitrary graph G = (V,E) and independent set S \subset V
# Step 2: Find an independent set U \subset V such that \alpha(G(U)) \leq V
# Setp 3: Collect vertices in V \ U as x1, x2, ..., x_k
# Step 4: ...
