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

from Graph.GraphPlot import GraphPlot                                           ## Plot the instance of G

from BalasYu.BScheme import BYBScheme                                           ## Access the class to perform the branch and bound algorithm
from BalasYu.RecSimpFix import RSF
from BalasYu.MISIP import MISIP

from BalasXue.WBScheme import BXWBScheme                                        ## Access the class to perform the weighted branch and bound algorithm 
from BalasXue.WMISIP import WMISIP

from Babel.BabelMethod import BWCCMethod

from networkx import erdos_renyi_graph
from scipy.io import mmread
import networkx as nx
import numpy as np
import random 

def exec_rsf_alg(G):
    rsf_model = RSF()
    simp_list = rsf_model.find_simplicial(G)
    F0, F1 = rsf_model.recursive_simplicial_fixing(G)
    return F0, F1

def exec_balas_yu_alg(G, case):
    BYMethod = BYBScheme()
    mis_output = BYMethod.branch_scheme(G, case)
    return mis_output

def exec_balas_xue_alg(G, W, case):
    BXMethod = BXWBScheme()
    wmis_output = BXMethod.branch_scheme(G, W, case)
    return wmis_output

def exec_babel_alg(G, W):
    BMethod = BWCCMethod(G, W) 
    BMethod.babel_scheme()

def main(argc, argv):

    G = erdos_renyi_graph(25, 0.5)

    print("Executing the Balas-Yu Branching Scheme\n")

    # Un-weighted Branching Scheme by Balas-Yu
    tol = 1e-8
    count, limit = 0, 10

    while True:
        opt_mis = exec_balas_yu_alg(G, 2)
        total_sum = 0
        for v in opt_mis:
            total_sum = total_sum + 1

        mis_model = MISIP(G)
        mis_model.optimize()

        if total_sum == mis_model.opt_cost(): 
            count = count + 1
            print(f"Case {count} / {limit}: Success!")
        else: 
            print(f"Case {count} / {limit}: Fail! Terminating at an invalid output ...\n")
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

        GPlot = GraphPlot()
        GPlot.disp_graph(G)

    print("Executing the Balas-Xue Branching Scheme\n")

    # Weighted Branching Scheme by Balas-Xue
    tol = 1e-8
    count, limit = 0, 10
    while True:
        W = {}
        for v in G.nodes: W[v] = random.uniform(1.5, 5.5)
        
        opt_wmis = exec_balas_xue_alg(G, W, 2)
        total_weight = 0
        for v in opt_wmis:
            total_weight = total_weight + W[v]

        wmis_model = WMISIP(G, W)
        wmis_model.optimize()

        A, B = set(wmis_model.opt_soln()), set(opt_wmis)
        if A.issubset(B) and B.issubset(A): 
            count = count + 1
            print(f"Case {count} / {limit}: Success!")
        else: 
            print(f"Case {count} / {limit}: Fail! Terminating at an invalid output ...\n")
            break
        
        if count == limit: 
            print(f"\nAll {limit} cases have passed! Great job!\n")
            break
        
    if count < limit:
        print(f"Expected Output:  {wmis_model.opt_soln()}")
        print(f"Branching Output: {opt_wmis}\n")

        print(f"Expected Weight:  {wmis_model.opt_cost()}")
        print(f"Branching Weight: {total_weight}\n")

        A, B = opt_wmis, wmis_model.opt_soln()
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

    # Weighted Clique Cover by Babel 
    print("Executing the Babel Algorithm\n")

    tol = 1e-8
    count, limit = 0, 10
    while True:
        W = {}
        for v in G.nodes: W[v] = random.randint(1, 51)

        wmis_output = exec_balas_xue_alg(G, W, 3)
        wmis_model = WMISIP(G, W)
        wmis_model.optimize()
        optimal_weight = wmis_model.opt_cost()

        total_weight = sum(W[v] for v in wmis_output)
        if abs(total_weight - optimal_weight) < 1e-8:
            count += 1 
            print(f"Case {count} / {limit}: Success!")
        else: 
            print(f"Case {count} / {limit}: Fail! Terminating at an invalid output ...\n")
            break

        if count == 10: 
            print(f"\nAll {count} cases passed! Great Job!\n")
            break

    if count < limit:
        print(f"Expected Output:  {wmis_model.opt_soln()}")
        print(f"Branching Output: {opt_wmis}\n")

        print(f"Expected Weight:  {wmis_model.opt_cost()}")
        print(f"Branching Weight: {total_weight}\n")

        A, B = opt_wmis, wmis_model.opt_soln()
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
    
if __name__ == "__main__":
    if len(sys.argv) < 2: 
        pass
        # print(f"Invalid argument count: {len(sys.argv)} - Try again ...")
        # exit()
    
    main(len(sys.argv), sys.argv)