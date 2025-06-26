import networkx as nx
from networkx.algorithms.approximation.clique import max_clique

# Reference: https://networkx.org/documentation/networkx-2.4/reference/algorithms/generated/networkx.algorithms.approximation.clique.max_clique.html

from random import choice
import itertools

from .MISIP import MISIP
from Graph.GraphPlot import GraphPlot
from .CCIP import CCIP

class GenUS:
    def __init__(self): 
        self.length = 26

    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: N/A
    #
    # Description: N/A
    #
    # Argument(s): N/A
    #
    # Return(s): N/A
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def indepSimplicial(self, G, S): 
        I, V_p = [], list(G.nodes())
        
        while V_p != []:
            v = choice(V_p)
            I.append(v)
            
            neighborhood = G.neighbors(v)
            V_p.remove(v)

            for v in neighborhood:
                if v in V_p: V_p.remove(v)
        
        return I

    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: N/A
    #
    # Description: N/A
    #
    # Argument(s): N/A
    #
    # Return(s): N/A
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def simplicial(self, G):
        simplicial_list = []
        
        for vertex in G.nodes():
            neighborhood = list(G.neighbors(vertex))                    # Open neighborhood N_{G'}(v)
            simplicial_status = True

            for edge in itertools.combinations(neighborhood, 2):        # Check if open neighborhood of v forms a clique
                if not G.has_edge(edge[0], edge[1]):
                    simplicial_status = False
                    break
            
            if simplicial_status: simplicial_list.append(vertex)

        return simplicial_list                                          # returns the set of vertices of G

    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: N/A
    #
    # Description: N/A
    #
    # Argument(s): N/A
    #
    # Return(s): N/A
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def recursive_simplicial_fixing(self, G):
        V, E = G.nodes(), G.edges()
        
        G_p  = G.copy()
        F0, F1 = [], []
        remove = {}
        for v in V: remove[v] = False
        
        while True:
            S = self.simplicial(G_p)
            D = self.indepSimplicial(G_p, S)
            
            for v in D:                                 # Update F0 and F1
                F1.append(v)
                for u in G_p.neighbors(v):
                    if u not in F0: F0.append(u)
            
            for v in D:                                 # Flag v as True if v \in N_{G_p}[v]
                remove[v] = True
                for u in G_p.neighbors(v): remove[u] = True
            
            R = []
            for v in G_p.nodes():
                if remove[v] == False: R.append(v)
            
            G_p = nx.induced_subgraph(G_p, R)
            
            if D == []: break
        
        return F0, F1
    
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: N/A
    #
    # Description: N/A
    #
    # Argument(s): N/A
    #
    # Return(s): N/A
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def chordal_method(self, G : nx):

        lot = GraphPlot()
        
        VnT, T = self.recursive_simplicial_fixing(G)
        print(f">>> {'Remaining vertex set: ':<{self.length}} {VnT}")
        print(f">>> {'Maximal independent set: ':<{self.length}} {T}")

        Gc = nx.complement(G)
        ISGc = nx.induced_subgraph(Gc, T)
  
        status = nx.is_chordal(ISGc)
        message = 'Is Chordal' if status else 'Is Not Chordal'            
        print(f">>> {'Original ISGc status: ':<{self.length}} {message}\n")

        # lot.disp_graph(G)

        GT = nx.induced_subgraph(G, T)
        print(f">>> {'Final set T: ':<{25}}  {T}\n")

        mis_model = MISIP(GT)
        mis_model.optimize()
        S = mis_model.opt_soln()
        print(f"\n>>> {'Maximum independent set S:':<{25}} {S}")

        clique_list = list(nx.find_cliques(GT))
        print(f">>> {'Full Clique List: ':<{26}} {clique_list}")

        MCC_model = CCIP(GT, clique_list)
        MCC_model.optimize()
        CC = MCC_model.opt_soln()

        print(f">>> {'Full Clique Cover: ':<{26}} {CC}\n")

        clique_dict = {}
        for idx, clique in enumerate(clique_list):
            clique_dict[idx] = clique.copy()

        # Almost correct, need to fix - find the bug
        for vertex in VnT: 
            neighborhood = list(G.neighbors(vertex))
            for idx in range(len(clique_list)):
                C_set, N_set = set(clique_dict[idx]), set(neighborhood)
                if C_set.issubset(N_set): 
                    # print(f"Clique: {C_set} | Neighborhood {neighborhood}")
                    # print(f"Appending {vertex} to {clique_dict[idx]}")
                    clique_dict[idx].append(vertex)
                    # print(f"Now: {clique_dict[idx]}\n")

        # G_cliques = list(nx.find_cliques(G))
        # print(f"\nClique List: {G_cliques}\n")

        # for key, val in clique_dict.items(): print(f"key: {key} - val: {val}")

        U = set([])
        for clique in clique_dict.values():
            print(f"clique: {set(clique)}")
            for v in clique: U.add(v)
        U = list(U)

        print(f"Final set U: {U}") 

        Gp = nx.induced_subgraph(G, U)
        mis_model = MISIP(Gp)
        mis_model.optimize()
        cost = mis_model.opt_cost()

        if (cost <= len(S)): print("Good output!")
        else: print("Bad output!")

        return S, U
    
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: N/A
    #
    # Description: N/A
    #
    # Argument(s): N/A
    #
    # Return(s): N/A
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def greedy_method(self, G : nx):
        mis_model = MISIP(G)
        mis_model.optimize()
        S = mis_model.opt_soln()

        # Greedy clique-covering algorithm 
        K_list, Gt = [[] for _ in range(len(S))], G 
        for idx, v in enumerate(S):
            neighbors = nx.neighbors(Gt, v)                          
            Gv = nx.induced_subgraph(G, neighbors)                      # Get the induced subgraph G[N[v]].

            clique = list(max_clique(Gv))                               # Get the largest clique in the list - greedy process (selecting vertices that maintain simplicial ordering on v)
            clique.append(v)                                            # Append the vertex v into the list. 
            clique = set(clique)

            nodes = set(Gt.nodes)
            node_update = list(nodes.difference(clique))                # Update the node list to generate a new induced subgraph. 

            Gt = nx.induced_subgraph(Gt, node_update)                   # Generate the induced subgraph with the subset of vertices

            clique = list(clique)
            K_list[idx] = clique

        for idx in range(len(K_list)): print(f"List {idx}: {K_list[idx]}")

        U = [v for list in K_list for v in list]
        print(f"U list: {U}")

        return S, U