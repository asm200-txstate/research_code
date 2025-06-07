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
from Graph.Graph import Graph                                                   ## Create an instance of G
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
    def __init__(self, G : Graph): 
        self.GPlot = nx.Graph()
        self.Graph = G

        V, E = self.Graph.get_all_v(), self.Graph.get_all_e()

        self.GPlot.add_nodes_from(V)
        self.GPlot.add_edges_from(E)

    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: disp_graph
    #
    # Description: Displays the graph G via netowrkx. 
    #
    # Argument(s): None
    #
    # Return(s): None
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def disp_graph(self): 
        pos = nx.circular_layout(self.GPlot, 2)
        nx.draw_networkx(self.GPlot, pos, width=2, node_size=800, font_size=12, font_color='white')

        plt.title(f"Induced Subgraph for $K_{{{len(self.Graph.get_all_v())}}}$")
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
    def disp_isgraph(self, Gt : Graph): # Before: def disp_ISG(self, U, Et):
        pos = nx.circular_layout(self.GPlot, 2)

        Vt = Gt.get_all_v()
        Et = Gt.get_all_e()
        # print("Gt vertices:", Gt.get_allV())
        # print("Gt vertices:", Gt.get_allE())

        args = {"node_size" : 800}
        nx.draw_networkx(self.GPlot, pos, width=3, font_size=18, font_color="white", **args)
        nx.draw_networkx_nodes(self.GPlot, pos, nodelist=Vt, node_color="tab:red", **args)
        nx.draw_networkx_edges(self.GPlot, pos, width=3, edgelist=Gt.get_all_e(), edge_color="tab:red", **args)

        legend_label = [
            Line2D([0], [0], marker='o', label=r'ISG: $\tilde{G} = (\tilde{V}, \tilde{E})$', markerfacecolor='tab:red', color='tab:red')
        ]
        plt.legend(handles=legend_label, loc='upper right')

        plt.title(r"Induced Subgraph (ISG) Plot on G = (V, E)")
        plt.show()