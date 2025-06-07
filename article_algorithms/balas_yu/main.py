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
from Graph.GenISG import GenISGraph                                         ## Create an instance of Gtilde (induced subgraph of G)
from Graph.Graph import Graph                                                   ## Create an instance of G
from BYBranchBound.BYBBStrat import BYBBStrat                                   ## Access the class to perform the branc and bound algorithm

def main(argc, argv):
    # RandG = GenGraph(int(argv[1]))
    # (V, E) = (RandG.gen_V(), RandG.gen_E())

    # Future task: See if one can make objects for vertices and edges
    V = [v+1 for v in range(10)]
    E = [[1,2], [2,3], [3,4], [4,5], [6,7], [7,8], [8,9], [9,10], [3,8]]
    G = Graph(V,E)

    BBStrat = BYBBStrat(G)
    BBStrat.find_mis()               # Find the maximal independent set - apply recursion

    # DispG = GraphPlot(G)
    # DispG.disp_graph() 

    ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####

    # # Providing an independent set S \subseteq V to G
    # S = [1,3,5]
    
    # # Creating an aribtrary induced subgraph (Goal: Check if GenISGraph and GraphPlot.disp_ISG() works correctly)
    # Vt = [1,2,3,8,9]
    # GenISG = GenISGraph(G, Vt)    # Provides the graph and set of vertices to generate the induced subgraph
    # Et = GenISG.gen_Et()          # Provides an induced subgrpah (Update, return a graph, not a set of edges)

    # ISG = Graph(Vt, Et)
    # DispISG = GraphPlot(ISG)

    # DispISG.disp_G()
    # DispG.disp_ISG(ISG)

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        pass
        # print(f"Invalid argument count: {len(sys.argv)} - Try again ...")
        # exit()
    
    main(len(sys.argv), sys.argv)