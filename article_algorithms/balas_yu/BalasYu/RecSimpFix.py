import networkx as nx
from random import choice
import itertools

from .MISIP import MISIP
from Graph.GraphPlot import GraphPlot

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

    def GenUS(self, G : nx):
        V, E = G.nodes(), G.edges()

        G = nx.Graph()
        G.add_nodes_from(V)
        G.add_edges_from(E)

        # Iteratively repeat algorithm until condition is satisfied
            
        chordal_count = 0
        while True:
            T0, T1 = self.recursive_simplicial_fixing(G)
            print(f">>> {'Remaining vertex set: ':<{self.length}} {T0}")
            print(f">>> {'Maximal independent set: ':<{self.length}} {T1}")

            Gc = nx.complement(G)
            ISGc = nx.induced_subgraph(Gc, T0)
            
            status = nx.is_chordal(ISGc)
            message = 'Is Chordal' if status else 'Is Not Chordal'
            
            print(f">>> {'Original ISGc status: ':<{self.length}} {message}\n")

            Tp = T0.copy()
            for t in T1:
                Tp.append(t)
                IGc = nx.induced_subgraph(Gc, Tp)

                status = nx.is_chordal(IGc)
                message = 'Is Chordal' if status else 'Is Not Chordal'
                
                # print(f">>> {f'ISGc status after adding {t}':<{27}} ... {message}")
                Tp.remove(t)

                if status: chordal_count += 1                                                   # Counting the cases appending t in T1\T0 to \overline{G}[T0] to remain chordal

            if chordal_count != 0: 
                print(">>> Try again ....\n")
                chordal_count = 0                                                               # Reset count and repeat process
            else: 
                print(">>> Final set found!\n")
                break

        Gp = nx.induced_subgraph(G, T0)
        print(f">>> {'Final set T0: ':<{25}}  {T0}\n")

        mis_model = MISIP(Gp)
        mis_model.optimize()
        S = mis_model.opt_soln()

        print(f"Maximum independent set S: {S}")

        clique_list = list(nx.find_cliques(Gp))
        print(clique_list)

        # Need to find the disjoint cliques where K_1 \cup ... \cup K_{|S|} = T0

        GPlot = GraphPlot()
        GPlot.disp_graph(Gp)