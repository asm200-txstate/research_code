import itertools
import networkx as nx

# max_clique information
# Reference: https://networkx.org/documentation/networkx-2.4/reference/algorithms/generated/networkx.algorithms.approximation.clique.max_clique.html

from random import choice
from networkx.algorithms.approximation.clique import max_clique

from .MISIP import MISIP
from Graph.GraphPlot import GraphPlot
from .CCIP import CCIP

class RSF:
    def __init__(self): self.length = 26

    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: N/A
    #
    # Description: N/A
    #
    # Argument(s): N/A
    #
    # Return(s): N/A
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def indepSimplicial(self, G : nx, S : list): 
        I, V_p = [], list(nx.induced_subgraph(G, S).nodes())
        
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
    def find_simplicial(self, G : nx):
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
    def recursive_simplicial_fixing(self, G : nx):
        V, E = G.nodes(), G.edges()
        
        G_p  = G.copy()
        F0, F1 = [], []
        remove = {}
        for v in V: remove[v] = False
        
        while True:
            S = self.find_simplicial(G_p)
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
