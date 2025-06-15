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

import sys
sys.dont_write_bytecode = True                                                  ## Prevent __pycache__ from being generated

from Graph.GenGraph import GenGraph                                             ## Randomly generate a graph G = (V,E)
from Graph.GraphPlot import GraphPlot                                           ## Plot the instance of G
from BalasYu.BranchScheme import BYBBStrat                                      ## Access the class to perform the branc and bound algorithm
from BalasYu.RecSimpFix import GenUS

import networkx as nx

def main(argc, argv):
    # RandG = GenGraph(int(argv[1]))
    # (V, E) = (RandG.gen_V(), RandG.gen_E())

    # Future task: See if one can make objects for vertices and edges
    V = [v+1 for v in range(10)]
    E = [[1,2], [2,3], [3,4], [4,5], [6,7], [7,8], [8,9], [9,10], [3,8]]
    
    G = nx.Graph()
    G.add_nodes_from(V)     # Defining the vertices to the graph 
    G.add_edges_from(E)     # Defining the edges to the graph

    # BBStrat = BYBBStrat()
    # BBStrat.branch_scheme(G)               # Find the maximal independent set - apply recursion

    # G_p = nx.induced_subgraph(G, [1,2,3,8,9])   # Sample induced subgraph

    # DispG = GraphPlot()
    # DispG.disp_graph(G) 
    # DispG.disp_isgraph(G, G_p) 

    RCF = GenUS()
    RCF.GenUS(G)

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        pass
        # print(f"Invalid argument count: {len(sys.argv)} - Try again ...")
        # exit()
    
    main(len(sys.argv), sys.argv)