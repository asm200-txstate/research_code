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
from BalasYu.MISIP import MISIP
from BalasYu.ChordalMethod import ChordalMethod

from BalasXue.WBScheme import BXWBScheme                                        ## Access the class to perform the weighted branch and bound algorithm 
from BalasXue.WGreedyMethod import WGMethod
from BalasXue.WMISIP import WMISIP
from BalasXue.WChordalMethod import WCMethod

from Babel.BabelMethod import BMethod

from SafeColor.gen_cliques import gen_cliques
from SafeColor.dual_ccip import dual_ccip
from SafeColor.wcc_heuristic import wcc_generator

from Max_WC.max_weight_cover import max_wc

from itertools import combinations
import networkx as nx
from networkx import erdos_renyi_graph
import random 

from random import randint

def main(argc, argv):

    G = erdos_renyi_graph(25, 0.5)

    # V = [v for v in range(2)]
    # E = [(0,1), (0,2)]
    # G = nx.Graph()
    # G.add_nodes_from(V)
    # G.add_edges_from(E)

    # V = [v for v in range(14)]
    # E = [(0, 1), (1, 3), (1, 4), (2, 3), (3, 4), (4, 5), (2,6), 
    #      (6,7), (3,7), (3,8), (4,7), (4,8), (7,8), (8,9), (5,9),
    #      (7,10), (10,11), (7,11), (8,12), (12,13), (8,13)]
    # G = nx.Graph()
    # G.add_nodes_from(V)
    # G.add_edges_from(E)

    BYMethod = BYBScheme()
    BYMethod.branch_scheme(G)

    # mis_model = MISIP(G)
    # mis_model.optimize()
    # print(f"Final Maximum IS: {mis_model.opt_soln()}")
    # print(f"Final MIS Size: {len(mis_model.opt_soln())}\n")

    # print("Final sets:")
    # BYMethod.disp_final_sets()

    GPlot = GraphPlot()
    GPlot.disp_graph(G)

    # CMethod = ChordalMethod(nx.complement(G))
    # CMethod.execute_cm()

    # U, _ = CMethod.gen_sets()
    # H = nx.induced_subgraph(G, U)

    # cc_model = CCIP(H, list(nx.find_cliques(H))) 
    # cc_model.optimize()
    # print(f"Optimal cost: {cc_model.opt_cost()}")
    # print(f"Optimal soln: {cc_model.opt_soln()}")

    # mis_model = MISIP(H)
    # mis_model.optimize()
    # print(f"Optimal cost: {mis_model.opt_cost()}")
    # print(f"Optimal soln: {mis_model.opt_soln()}")

    # G = nx.complement(nx.cycle_graph(5))
    # Hhat = nx.complement(G)
    # print(f"Is Chordal: {nx.is_chordal(Hhat)}")

    # GPlot = GraphPlot()
    # GPlot.disp_graph(Hhat)

    # print("Cliques in G-complement:")
    # print("Cliques: ", list(nx.find_cliques(nx.complement(G))))

    # clique_list = list(nx.find_cliques(nx.complement(G)))
    # for clique in clique_list: 
    #     print(f"Clique: {clique} - Chordal Status: {nx.is_chordal(nx.induced_subgraph(G, clique))}")

    # GPlot = GraphPlot()
    # GPlot.disp_graph(nx.complement(G))
    # # GPlot.disp_isgraph(G, H)

    # BYMethod = BYBScheme()
    # BYMethod.branch_scheme(G)

    # return

    # W = {}
    # for v in G.nodes: W[v] = randint(1, 10)

    # BM = BMethod(G, W)
    # BM.babel_method()
    # BM.node_elimination()
    # BM.branching_scheme()

    # GenC = gen_cliques(G)

    # mis_set = set()
    # GenC.find_mis(mis_set, [], 1)

    # mis_list = []
    # for curr_list in mis_set: mis_list.append(list(curr_list))
    # # print(f"MIS List: {mis_list}")
    # # print(f"MIS List length: {len(mis_list)}")

    # S_prime_set = set()
    # for clique in mis_list: 
    #     S_prime_set.add(frozenset(random.choice(mis_list)))

    # S_prime = []
    # for element in S_prime_set: S_prime.append(list(element))

    # CCIP_dual = dual_ccip(G, S_prime)
    # CCIP_dual.optimize()

    # opt_cost, vertex_cost, clique_cost = CCIP_dual.opt_cost()
    # print(f"Optimal Cost: {opt_cost}")

    # soln_vertex, soln_clique = CCIP_dual.opt_soln()
    # for v in soln_vertex: print(f"Vertex Output: {v}")
    # for clique in soln_clique: print(f"Clique Output: {clique}")

    # for idx, cost in enumerate(vertex_cost): print(f"Node idx: {idx+1} - {cost}")
    # for idx, cost in enumerate(clique_cost): print(f"Clique idx: {S_prime[idx]} \t - {cost}")

    # print("")
    # weighted_cc = max_wc(G, W)

    # temp_dict = {}
    # for v in G: temp_dict[v] = nx.degree(G, v)
    # R = list(dict(sorted(temp_dict.items(), key = lambda item : item[1], reverse=True)))
    
    # print(f"R: {R}")
    # weighted_cc.ColorSortWeight(R)
    # weighted_cc.Expand(R)

    # # weighted_cc.Expand()
    # # weighted_cc.ColorSortWeight()

    # # seen_dict = {}
    # # for v in G.nodes: seen_dict[v] = False
    # # gen_wcc = wcc_generator(G, W, seen_dict)
    # # gen_wcc.wwc_heuristic()
    # # gen_wcc.weighted_cliques()

    # # Define the dual variable \pi in the Safe Color notes. 
    # pi = vertex_cost

    # # print(f"PI Length: {len(pi)} - S_prime Length: {len(S_prime)}")
    # print(f"PI: {pi}")
    # print(f"S_prime: {S_prime}")

    # S_hat = []
    # for clique in mis_list:
    #     if clique not in S_prime: S_hat.append(clique)
    
    # print("Cliques in S_hat := S \ S_prime (where S := mis_list)")
    # for clique in S_hat: 
    #     print(f"Clique: {clique}")
    #     sum = 0
    #     for v in clique: sum += pi[v-1]
    #     if sum > 1: print("We hit pi(S) > 1")

    # # GPlot = GraphPlot()
    # # GPlot.disp_weight_graph(G, W)

    # # # BBStrat = BYBScheme()
    # # # BBStrat.branch_scheme(G)                        # Find the maximal independent set - apply recursion
    
    # # WBBStrat = BXWBScheme()
    # # WBBStrat.branch_scheme(G, W)

    # # WCM = WCMethod(G, W)
    # # WCM.wc_method()
    
if __name__ == "__main__":
    if len(sys.argv) < 2: 
        pass
        # print(f"Invalid argument count: {len(sys.argv)} - Try again ...")
        # exit()
    
    main(len(sys.argv), sys.argv)