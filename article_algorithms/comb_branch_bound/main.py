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
from BalasYu.RecSimpFix import RSF
from BalasYu.CCIP import CCIP

from BalasYu.BScheme import BYBScheme                                           ## Access the class to perform the branch and bound algorithm
from BalasXue.WBScheme import BXWBScheme                                        ## Access the class to perform the weighted branch and bound algorithm 
from BalasXue.WGreedyMethod import WGMethod
from BalasXue.WMISIP import WMISIP

import networkx as nx
from random import randint

def main(argc, argv):
    # RandG = GenGraph(int(argv[1]))
    # (V, E) = (RandG.gen_V(), RandG.gen_E())

    # Future task: See if one can make objects for vertices and edges
    # V = [v+1 for v in range(10)]
    # E = [[1,2], [2,3], [3,4], [4,5], [6,7], [7,8], [8,9], [9,10], [3,8]]          # Edge set 1

    # E = [[1,2], [1,3], [1,6], [2,4], [2,7], [3,5], [3,8], [4,5], [4,9], [5,10],   # Edge set 2
    #      [6,7], [6,8], [7,9], [8,10], [9,10],
    #      [3,4], [8,9]]                                                            # Note: Added edges to make K_3 induced subgraph

    # E = [[1,3], [1,4], [2,4], [2,5], [3,5],                                       # Edge set 3
    #      [1,6], [2,7], [3,8], [4,9], [5,10],
    #      [6,7], [7,8], [8,9], [9,10], [10,6]]

    # E = [[1,2], [1,6], [1,8],                                                     # Edge set 4
    #      [2,3], [2,6], [2,7], [2,10],
    #      [3,4], [3,5], [3,8], [3,9],
    #      [4,6], [4,10],
    #      [5,6], [5,7], [5,10],
    #      [6,9], 
    #      [7,8], [7,9],
    #      [8,9], [8,10],
    #      [9,10]]

    V = [v+1 for v in range(10)]
    E = [[1,2], [2,3], [3,4], [4,5], [6,7], [7,8], [8,9], [9,10], [3,8]]          
    
    G = nx.Graph()
    G.add_nodes_from(V)
    G.add_edges_from(E)

    # BBStrat = BYBScheme()
    # BBStrat.branch_scheme(G)                        # Find the maximal independent set - apply recursion

    # New Task: In the algorithm  Balas & Xue, we're dealing with weighted graphs, so define integer weights. 
    # While you can have real weights, let's keep it simple and make them integer. 
    
    W = {}
    for v in G.nodes: W[v] = randint(0, 10)
    
    # WBBStrat = BXWBScheme()
    # WBBStrat.branch_scheme(G, W)

    WGM = WGMethod(G, W)
    WGM.wg_method()

    U, S = WGM.gen_sets()
    print(f"\nSet U: {U}")
    print(f"Set S: {S}")

    K_list = WGM.gen_cliques()
    print(f"K list: {K_list}")

    is_graph = nx.induced_subgraph(G, U)

    wmis_model = WMISIP(is_graph, W)
    wmis_model.optimize()
    opt_nodes = wmis_model.opt_soln()

    S_weight, GU_weight = 0, 0

    for v in S: S_weight += W[v]
    for v in opt_nodes: GU_weight += W[v]
        
if __name__ == "__main__":
    if len(sys.argv) < 2: 
        pass
        # print(f"Invalid argument count: {len(sys.argv)} - Try again ...")
        # exit()
    
    main(len(sys.argv), sys.argv)