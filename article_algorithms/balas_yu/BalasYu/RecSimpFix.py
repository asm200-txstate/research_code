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
    
    def chordal_method(self, G : nx):
        V, E = G.nodes(), G.edges()

        G = nx.Graph()
        G.add_nodes_from(V)
        G.add_edges_from(E)

        # Iteratively repeat algorithm until condition is satisfied
        
        chordal_count = 0
        while True:
            T, VnT = self.recursive_simplicial_fixing(G)
            print(f">>> {'Remaining vertex set: ':<{self.length}} {VnT}")
            print(f">>> {'Maximal independent set: ':<{self.length}} {T}")

            Gc = nx.complement(G)
            ISGc = nx.induced_subgraph(Gc, T)
            
            status = nx.is_chordal(ISGc)
            message = 'Is Chordal' if status else 'Is Not Chordal'
            
            # print(f">>> {'Original ISGc status: ':<{self.length}} {message}\n")

            Tp = T.copy()
            for t in VnT:
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

        Gp = nx.induced_subgraph(G, T)
        print(f">>> {'Final set T: ':<{25}}  {T}\n")

        mis_model = MISIP(Gp)
        mis_model.optimize()
        S = mis_model.opt_soln()

        print(f"\n>>> {'Maximum independent set S:':<{25}} {S}")

        clique_list = list(nx.find_cliques(Gp))
        print(f">>> {'Full Clique List: ':<{26}} {clique_list}")

        # print(">>> Comination List: \n")
        final_clist = None

        for c_list in itertools.combinations(clique_list, len(S)):
            # print(f">>> Current Combination: {c_list}")
            cand_list = list(set([item for sublist in c_list for item in sublist]))               # Collect the vertices to the clique combination

            if list(Gp.nodes) == cand_list:                                                       # Check if the combination equals the nodes to the induced subgraph G'
                final_clist = list(c_list)
                break

        print(f">>> {'Clique Cover List: ':<{26}} {final_clist}\n")

        for t in VnT:
            print(f"Current node: {t}")
            print(f"{f'Neighborhood at {t}: ':<{20}} {list(nx.neighbors(G, t))}\n")

        for clique in final_clist:
            print(f"Clique: {clique}")

        print("")

        clique_dict = {}
        for key in final_clist:
            clique_dict[tuple(key)] = list(key)

        for t in T:
            for clique in final_clist:
                Nt = list(nx.neighbors(G, t))
                if set(clique).issubset(Nt):
                    clique_dict[tuple(clique)].append(t)

        for key, val in clique_dict.items():
            print(f"{f'Before: {list(key)}':<{14}} -> {f'After: {val}':<{10}}")

        Eu = []
        for key, E in clique_dict.items(): 
            for v in E: Eu.append(v)

        print(f"\nEu: {Eu}")
        Gu = nx.induced_subgraph(G, Eu)

        # GPlot = GraphPlot()
        # GPlot.disp_graph(Gu)

        return
    
    def greedy_method(self):
        pass