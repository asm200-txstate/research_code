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

    # E = [[1,3], [1,4], [2,4], [2,5], [3,5],
    #      [1,6], [2,7], [3,8], [4,9], [5,10],
    #      [6,7], [7,8], [8,9], [9,10], [10,6]]

    E = [[1,2], [1,6], [1,8],
         [2,3], [2,6], [2,7], [2,10],
         [3,4], [3,5], [3,8], [3,9],
         [4,6], [4,10],
         [5,6], [5,7], [5,10],
         [6,9], 
         [7,8], [7,9],
         [8,9], [8,10],
         [9,10]]

    # GenG = GenGraph(18)
    # V, E = GenG.gen_V(), GenG.gen_E()

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
    RCF.chordal_method(G)

    # Minor update to GenGraph.gen_E() method
    # GenG = GenGraph(8)
    # V = GenG.gen_V() 
    # E = GenG.gen_E()
    # G.add_nodes_from(V)
    # G.add_edges_from(E)

    # DispG = GraphPlot()
    # DispG.disp_graph(G)

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        pass
        # print(f"Invalid argument count: {len(sys.argv)} - Try again ...")
        # exit()
    
    main(len(sys.argv), sys.argv)