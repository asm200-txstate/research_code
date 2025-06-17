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

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx

class GraphPlot:
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: __init__ (Driver)
    #
    # Description: Initializes the graph G = (V,E). Defines an instance 
    #               of the graph G and initializes the vertex and edge sets,
    #               V and E, respectively, via networkx. 
    #
    # Argument(s):
    #    * V: The set of vertices to graph G
    #    * E: The set of edges to graph G 
    #
    # Return(s): None
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def __init__(self): 
        pass

        # self.GPlot = nx.Graph()
        # self.Graph = G

        # V, E = self.Graph.get_all_v(), self.Graph.get_all_e()

        # self.GPlot.add_nodes_from(V)
        # self.GPlot.add_edges_from(E)

    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: disp_graph
    #
    # Description: Displays the graph G via netowrkx. 
    #
    # Argument(s): None
    #
    # Return(s): None
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def disp_graph(self, G : nx): 
        pos = nx.circular_layout(G, 2)
        nx.draw_networkx(G, pos, width=2, node_size=800, font_size=12, font_color='white')
        plt.title(f"Induced Subgraph for $K_{{{len(G.nodes())}}}$")
        plt.show()

    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: disp_isgraph
    #
    # Description:  Displays an induced subgraph of G, called G-tilde (or \tilde{G}) via netwrokx. 
    #               A caption is used to specify G-tilde.  
    #
    # Argument(s): 
    #  * Gt: Abbreviated as Gtilde, or \tilde{G}, Gt is an induced subgraph to G (or self.Graph)
    #
    # Return(s): None
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def disp_isgraph(self, G, Gt): # Before: def disp_ISG(self, U, Et):
        pos = nx.circular_layout(G, 2)

        Vt = Gt.nodes()
        Et = Gt.edges()

        args = {"node_size" : 800}
        nx.draw_networkx(G, pos, width=3, font_size=18, font_color="white", **args)
        nx.draw_networkx_nodes(G, pos, nodelist=Vt, node_color="tab:red", **args)
        nx.draw_networkx_edges(G, pos, width=3, edgelist=Et, edge_color="tab:red", **args)

        legend_label = [
            Line2D([0], [0], marker='o', label=r'ISG: $\tilde{G} = (\tilde{V}, \tilde{E})$', markerfacecolor='tab:red', color='tab:red')
        ]
        plt.legend(handles=legend_label, loc='upper right')

        plt.title(r"Induced Subgraph (ISG) Plot on G = (V, E)")
        plt.show()
        return
    
    # Task: Add a disp_ind_isgraph() method ...
    # Goal: Help see what's considered the candidate vertex, xi, in not_N(xi)