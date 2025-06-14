import networkx as nx
from random import choice
import itertools

from .MISIP import MISIP

class GenUS:
    def __init__(self, G):
        self.G = G

    def indepSimplicial(self, G, S): # Update with algorithm 2 in lecture notes
        I, V_p = [], list(G.nodes())
        
        while V_p != []:
            v = choice(V_p)
            I.append(v)
            
            neighborhood = G.neighbors(v)
            V_p.remove(v)

            for v in neighborhood:
                if v in V_p: V_p.remove(v)
        
        return I

    def simplicial(self, G):
        simplicial_dict = {}
        
        for vertex in G.nodes():
            simplicial_dict[vertex] = False
            simplicial_count = 0
            neighborhood = list(G.neighbors(vertex)) # Open neighborhood N_{G'}(v)
                    
            is_simplicial = True
            for edge in itertools.combinations(neighborhood, 2): # Check if neighborhood of v forms a clique
                if not G.has_edge(edge[0], edge[1]):
                    is_simplicial = False
                    break
            
            if is_simplicial:
                simplicial_dict[vertex] = True
                simplicial_count += 1
            
    #    print(f"Final simplicial vertex count: {simplicial_count}")
        
        return [v for v in G.nodes() if simplicial_dict[v] == True] # returns the set of vertices of G

    def recursive_simplicial_fixing(self, G):
        V, E = G.nodes(), G.edges()
        
        G_p  = G.copy()
        F0, F1 = [], []
        remove = {}
        for v in V: remove[v] = False
        
        while True:
            S = self.simplicial(G_p)
            D = self.indepSimplicial(G_p, S)
            
            for v in D:
                F1.append(v)
                for u in G_p.neighbors(v):
                    if u not in F0: F0.append(u)
            
            for v in D:
                remove[v] = True
                for u in G_p.neighbors(v): remove[u] = True
            
            R = []
            for v in G_p.nodes():
                if remove[v] == False: R.append(v)
            
            G_p = nx.induced_subgraph(G_p, R)
            
            if D == []: break
        
        return F0, F1

    def GenUS(self):
        V, E = self.G.get_all_v(), self.G.get_all_e()

        G = nx.Graph()
        G.add_nodes_from(V)
        G.add_edges_from(E)
        
        F0, F1 = self.recursive_simplicial_fixing(G)
        
        print("Success!")
        print(f"Excess:      {F0}")
        print(f"Independent: {F1}")
        
        G_c = nx.complement(G)
        
        ISG_c = nx.induced_subgraph(G_c, F1)
        status = nx.is_chordal(ISG_c)
        print(f"ISG_c Chordal Status: {status}")

        GenISG = GenISGraph()
        GT = GenISG.gen_isgraph(self.G, F1)

        mis_model = MISIP(GT)
        mis_model.optimize()
        S = mis_model.opt_soln()

        print(f"Maximum independent set S: {S}")
