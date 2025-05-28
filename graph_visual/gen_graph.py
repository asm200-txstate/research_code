# Name: gen_visual.py
# Description: Generate a randomized graph that's an induced subgraph to a complete
#              graph G = (V,E). The following graph is displayed to the graph. 

import sys
import networkx as nx
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy as GRB
from random import randint

