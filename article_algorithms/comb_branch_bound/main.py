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

import json

from Graph.GenGraph import GenGraph                                             ## Randomly generate a graph G = (V,E)
from Graph.GraphPlot import GraphPlot                                           ## Plot the instance of G

from BalasYu.RecSimpFix import RSF
from BalasYu.CCIP import CCIP
from BalasYu.BScheme import BYBScheme                                           ## Access the class to perform the branch and bound algorithm
from BalasYu.MISIP import MISIP
from BalasYu.ChordalMethod import CMethod

from BalasXue.WBScheme import BXWBScheme                                        ## Access the class to perform the weighted branch and bound algorithm 
from BalasXue.WGreedyMethod import WGMethod
from BalasXue.WMISIP import WMISIP
from BalasXue.WChordalMethod import WCMethod

from Babel.BabelMethod import BMethod

from SafeColor.gen_cliques import gen_cliques
from SafeColor.dual_ccip import dual_ccip
from SafeColor.wcc_heuristic import wcc_generator

from Max_WC.max_weight_cover import max_wc

from networkx import erdos_renyi_graph
from itertools import combinations
import networkx as nx
import random 

from random import randint
import numpy as np

def exec_rsf_alg(G):
    rsf_model = RSF()
    simp_list = rsf_model.find_simplicial(G)
    F0, F1 = rsf_model.recursive_simplicial_fixing(G)
    return F0, F1

def exec_balas_yu_alg(G):
    BYMethod = BYBScheme()
    mis_output = BYMethod.branch_scheme(G, 2)
    return mis_output

def exec_balas_xue_alg(G, W):
    BXMethod = BXWBScheme()
    wmis_output = BXMethod.branch_scheme(G, W, 1)
    return wmis_output

def exec_babel_alg():
    pass

def main(argc, argv):

    G = erdos_renyi_graph(30, 0.5)

    # Weighted branching scheme by Balas-Xue  
    count, limit = 0, 500
    while True:
        W = {}
        for v in G.nodes: W[v] = 1 # randint(1, 10) 
    
        opt_mis = exec_balas_yu_alg(G)
        total_weight = 0
        for v in opt_mis:
            total_weight = total_weight + 1

        mis_model = MISIP(G)
        mis_model.optimize()

        if total_weight == mis_model.opt_cost(): 
            count = count + 1
            print(f"{count} of the {limit}: Success!")
        else: 
            print(f"{count} of the {limit}: Fail! Terminating at an invalid output ...\n")
            break

        if count == limit: 
            print(f"\nAll {limit} cases have passed! Great job!\n")
            break

    if count < limit:
        print(f"Expected Output:  {mis_model.opt_soln()}")
        print(f"Branching Output: {opt_mis}\n")

        print(f"Expected Weight:  {mis_model.opt_cost()}")
        print(f"Branching Weight: {total_weight}\n")

        A, B = opt_mis, mis_model.opt_soln()
        AnB, BnA = [], []

        for v in A:
            if v not in B: AnB.append(v)

        for v in B:
            if v not in A: BnA.append(v)

        if AnB == []: print("A is a subset of B\n")
        else:
            print("A is not a subset of B - Algorithm \ Expected")
            print(f"Missing entries: {AnB}\n")
        if BnA == []: print(print("B is a subset of A\n"))
        else:
            print("B is not a subset of A - Expected \ Algorithm")
            print(f"Missing entries: {BnA}\n")

        symm_diff = list(set(A).symmetric_difference(B))
        
        print(f"Vertices: {G.nodes}")
        print(f"Edges: {G.edges}")
        print(f"Weights: {W}")

        GPlot = GraphPlot()
        GPlot.disp_weight_graph(G, W)

    # AB_union = list(set(A).union(B))
    # v_list = list(set(A).union(B))

    # print(f"v_list: {v_list}")
    # print(f"AB_union: {AB_union}")

    # *****************************************************************

    # F0, F1 = exec_rsf_alg(G)
    # print(f"F0 Set - Length: {len(F0)}")
    # print(f"F1 Set - Length: {len(F1)}\n")  

    # isgraph = nx.induced_subgraph(G, list(set(G.nodes).difference(set(F1).union(F0))))
    # mis_list = exec_balas_yu_alg(isgraph)

    # for key, curr_mis_list in mis_dict.items():
    #     GPlot = GraphPlot()
    #     GPlot.vertex_labels_P2(G, F0, F1, curr_mis_list, key) 

    # *****************************************************************

    return

    print("Without using the RSF Model ...\n")

    BYMethod = BYBScheme()
    status = BYMethod.branch_scheme(G, 1)

    print("\nUsing the RSF Model ...\n")

    rsf_model = RSF()
    simp_list = rsf_model.find_simplicial(G)
    F0, F1 = rsf_model.recursive_simplicial_fixing(G)
    # print(f"O entries: {F0}")
    # print(f"1 entries: {F1}")

    print(f"Simplicial Vertices: {simp_list}\n")
    print(f"Length |V|: {len(G.nodes)}")
    print(f"Length |F0|: {len(F0)}")
    print(f"Length |F1|: {len(F1)}")

    node_list = set(list(G.nodes)).difference(set(F0).union(F1))
    ISG = nx.induced_subgraph(G, node_list)

    # G = nx.florentine_families_graph()
    BYMethod = BYBScheme()
    status = BYMethod.branch_scheme(ISG, 1)
    # if not status: print("******************** Invalid output ...")
    # else: print("******************** Good output!")

    print(f"\nLength |V|: {len(ISG.nodes)}")
    print(f"Length |F0|: {len(F0)}")
    print(f"Length |F1|: {len(F1)}")
    print(f"Vertices in F1: {F1}")

    V_orig, V_update = list(G.nodes), list(G.nodes)
    for v in V_orig:
        if v in F0 or v in F1: V_update.remove(v)

    mis_model = MISIP(G)
    mis_model.optimize()
    print(f"Optimal solution on original G: {mis_model.opt_cost()}")

    GPlot = GraphPlot()
    GPlot.disp_rsf_colors(G, F0, F1, V_update)
    
if __name__ == "__main__":
    if len(sys.argv) < 2: 
        pass
        # print(f"Invalid argument count: {len(sys.argv)} - Try again ...")
        # exit()
    
    main(len(sys.argv), sys.argv)

# Expected Output:  [0, 1, 2, 4, 5, 7, 9]
# Branching Output: [0, 1, 2, 4, 5, 6, 7]