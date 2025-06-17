import networkx as nx
from random import choice
import itertools

from .MISIP import MISIP
from Graph.GraphPlot import GraphPlot
from .CCIP import CCIP

class GenUS:
    def __init__(self): 
        self.length = 26

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
    
    def chordal_method(self, G : nx):

        GPlot = GraphPlot()

        VnT, T = self.recursive_simplicial_fixing(G)
        print(f">>> {'Remaining vertex set: ':<{self.length}} {VnT}")
        print(f">>> {'Maximal independent set: ':<{self.length}} {T}")

        Gc = nx.complement(G)
        ISGc = nx.induced_subgraph(Gc, T)
        
        status = nx.is_chordal(ISGc)
        message = 'Is Chordal' if status else 'Is Not Chordal'            
        print(f">>> {'Original ISGc status: ':<{self.length}} {message}\n")

        # GPlot.disp_graph(G)

        Gp = nx.induced_subgraph(G, T)
        print(f">>> {'Final set T: ':<{25}}  {T}\n")

        mis_model = MISIP(Gp)
        mis_model.optimize()
        S = mis_model.opt_soln()

        print(f"\n>>> {'Maximum independent set S:':<{25}} {S}")

        clique_list = list(nx.find_cliques(Gp))
        print(f">>> {'Full Clique List: ':<{26}} {clique_list}")

        MCC_model = CCIP(Gp, clique_list)
        MCC_model.optimize()
        CC = MCC_model.opt_soln()

        print(f">>> {'Full Clique Cover: ':<{26}} {CC}\n")

        return
    
    def greedy_method(self):
        pass