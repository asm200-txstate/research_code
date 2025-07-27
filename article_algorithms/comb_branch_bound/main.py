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

from SafeColor.gen_cliques import gen_cliques
from SafeColor.dual_ccip import dual_ccip
from SafeColor.wcc_heuristic import wcc_generator

from Max_WC.max_weight_cover import max_wc

import networkx as nx
import random 

from random import randint

def find_mis(G, mis_set, curr_nodes, start_node):

    if start_node >= len(G.nodes()):    # All nodes in G have been seen
        try: 
            curr_list = list(nx.maximal_independent_set(G, curr_nodes))    # Check if curr_nodes list is an stable set
            mis_set.add(frozenset(curr_list))
        except: pass                                                       # Invalid set - not a stable set. Continue moving forward. 
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

    GenC = gen_cliques(G)

    mis_set = set()
    GenC.find_mis(mis_set, [], 1)

    mis_list = []
    for curr_list in mis_set: mis_list.append(list(curr_list))
    # print(f"MIS List: {mis_list}")
    # print(f"MIS List length: {len(mis_list)}")

    S_prime_set = set()
    for clique in mis_list: 
        S_prime_set.add(frozenset(random.choice(mis_list)))

    S_prime = []
    for element in S_prime_set: S_prime.append(list(element))

    CCIP_dual = dual_ccip(G, S_prime)
    CCIP_dual.optimize()

    opt_cost, vertex_cost, clique_cost = CCIP_dual.opt_cost()
    print(f"Optimal Cost: {opt_cost}")

    soln_vertex, soln_clique = CCIP_dual.opt_soln()
    for v in soln_vertex: print(f"Vertex Output: {v}")
    for clique in soln_clique: print(f"Clique Output: {clique}")

    for idx, cost in enumerate(vertex_cost): print(f"Node idx: {idx+1} - {cost}")
    for idx, cost in enumerate(clique_cost): print(f"Clique idx: {S_prime[idx]} \t - {cost}")

    print("")
    weighted_cc = max_wc(G, W)
    weighted_cc.ColorSortWeight()

    # seen_dict = {}
    # for v in G.nodes: seen_dict[v] = False
    # gen_wcc = wcc_generator(G, W, seen_dict)
    # gen_wcc.wwc_heuristic()
    # gen_wcc.weighted_cliques()

    return

    # Define the dual variable \pi in the Safe Color notes. 
    pi = vertex_cost

    # print(f"PI Length: {len(pi)} - S_prime Length: {len(S_prime)}")
    print(f"PI: {pi}")
    print(f"S_prime: {S_prime}")

    S_hat = []
    for clique in mis_list:
        if clique not in S_prime: S_hat.append(clique)
    
    print("Cliques in S_hat := S \ S_prime (where S := mis_list)")
    for clique in S_hat: 
        print(f"Clique: {clique}")
        sum = 0
        for v in clique: sum += pi[v-1]
        if sum > 1: print("We hit pi(S) > 1")

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