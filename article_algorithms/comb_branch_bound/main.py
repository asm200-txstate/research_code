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
sys.setrecursionlimit(1000000)

from Graph.GenGraph import GenGraph                                             ## Randomly generate a graph G = (V,E)
from Graph.GraphPlot import GraphPlot                                           ## Plot the instance of G

from BalasYu.RecSimpFix import RSF
from BalasYu.CCIP import CCIP
from BalasYu.BScheme import BYBScheme                                           ## Access the class to perform the branch and bound algorithm

from BalasXue.WBScheme import BXWBScheme                                        ## Access the class to perform the weighted branch and bound algorithm 
from BalasXue.WGreedyMethod import WGMethod
from BalasXue.WMISIP import WMISIP
from BalasXue.WChordalMethod import WCMethod

from Babel.BabelMethod import BMethod

import networkx as nx
from random import randint

def find_mis(G, mis_set, curr_nodes, start_node):

    if start_node >= len(G.nodes()):    # All nodes in G have been seen
        try: 
            curr_list = list(nx.maximal_independent_set(G, curr_nodes))    # Check if curr_nodes list is an stable set
            mis_set.add(frozenset(curr_list))
        except: pass                                                        # Invalid set - not a stable set. Continue moving forward. 
        return

    # Iterate through every vertex in G (starting from start_node)
    for v in list(G.nodes())[start_node:]:
        if v in curr_nodes: continue
        curr_nodes.append(v)
        find_mis(G, mis_set, curr_nodes, start_node + 1)
        curr_nodes.remove(v)

    # Make recursive calls without appending start_node
    find_mis(G, mis_set, curr_nodes, start_node + 1)

def main(argc, argv):
    V = [v+1 for v in range(10)]
    E = [[1,2], [2,3], [3,4], [4,5], [6,7], [7,8], [8,9], [9,10], [3,8]]          

    G = nx.Graph()
    G.add_nodes_from(V)
    G.add_edges_from(E)

    W = {}
    for v in G.nodes: W[v] = randint(1, 10)

    BM = BMethod(G, W)
    BM.babel_method()
    BM.node_elimination()
    BM.branching_scheme()

    mis_list = set()
    find_mis(G, mis_list, [], 1)

    final_list = []
    for curr_list in mis_list: final_list.append(list(curr_list))
    print(f"List: {final_list} \nLength: {len(final_list)}")

    

    # GPlot = GraphPlot()
    # GPlot.disp_weight_graph(G, W)

    # # BBStrat = BYBScheme()
    # # BBStrat.branch_scheme(G)                        # Find the maximal independent set - apply recursion
    
    # WBBStrat = BXWBScheme()
    # WBBStrat.branch_scheme(G, W)

    # WCM = WCMethod(G, W)
    # WCM.wc_method()
    
if __name__ == "__main__":
    if len(sys.argv) < 2: 
        pass
        # print(f"Invalid argument count: {len(sys.argv)} - Try again ...")
        # exit()
    
    main(len(sys.argv), sys.argv)