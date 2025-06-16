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

                if status: chordal_count += 1                                                  # Counting the cases appending t in T1\T0 to \overline{G}[T0] to remain chordal

            if chordal_count != 0: 
                print(">>> Try again ....\n")
                chordal_count = 0                                                              # Reset count and repeat process
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

        MCC_model = CCIP(Gp, clique_list)
        MCC_model.optimize()
        CC = MCC_model.opt_soln()

        print(f">>> {'Full Clique Cover: ':<{26}} {CC}\n")

        clique_dict = {}                                                                       
        for key in CC:
            clique_dict[tuple(key)] = list(key)

        # Sequentially adding vertices v \in V\T to cliques containing vertices in N(v), giving cliques \hat{K_{1}}, ..., \hat{K_{|S|}}
        for t in T:
            for clique in CC:
                Nt = list(nx.neighbors(G, t))
                if set(clique).issubset(Nt):
                    clique_dict[tuple(clique)].append(t)
        
        for key, val in clique_dict.items():
            print(f"{f'Before: {list(key)}':<{14}} -> {f'After: {val}':<{10}}")

        U = []
        for key, E in clique_dict.items(): 
            for v in E: U.append(v)

        print(f"\n{'>>> Vertex set U: ':<{29}} {U}")                                                                    # Viewing the vertex set U where U is the union of \hat{K_{1}}, ..., \hat{K_{|S|}}
        Gu = nx.induced_subgraph(G, U)
        
        MIS_model = MISIP(Gu)
        MIS_model.optimize()
        if MIS_model.opt_cost() <= len(S): print(f">>> {'Final Result:':<{25}} Valid, a(G[U]) <= |S|")
        else: print(f">>> {'Final Result:':<{25}} Invalid, a(G[U]) > |S|")

        return
    
    def greedy_method(self):
        pass