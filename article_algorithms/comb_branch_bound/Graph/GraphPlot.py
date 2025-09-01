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
    # Argument(s): None
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
    # Description: Displays the graph G via netowrkx by displaying only their vertex numbers. 
    #
    # Argument(s): 
    #    * G: The graph G being displayed
    #
    # Return(s): None
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def disp_graph(self, G : nx): 
        # pos = nx.circular_layout(G, 2)
        # nx.draw_networkx(G, pos, width=2, node_size=800, font_size=12, font_color='white')
        nx.draw_networkx(G, width=2, node_size=500, font_size=8, font_weight='bold', font_color='white')
        plt.title(f"Induced Subgraph for $K_{{{len(G.nodes())}}}$")
        plt.show()

    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: disp_weight_graph
    #
    # Description: Displays the graph G via netowrkx by displaying both the vertex number and
    #              their weights. 
    #
    # Argument(s): 
    # * G: The graph G being displayed
    # * W: The dictionary mapping vertices to their weights in G
    #
    # Return(s): None
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****

    def disp_weight_graph(self, G : nx, W : dict):
        pos = nx.circular_layout(G, 2)
        node_label = {v : f"V: {v} \nW: {W[v]}" for v in G.nodes}
        nx.draw_networkx(G, pos, width=2, node_size=850, font_size=8, font_color='white', labels=node_label, with_labels=True, font_weight='bold') 
        plt.title(f"Induced Subgraph for $K_{{{len(G.nodes())}}}$")
        plt.show()

    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: disp_isgraph
    #
    # Description:  Displays an induced subgraph of G, called G-tilde (or \tilde{G}) via netwrokx. 
    #               A caption is used to specify G-tilde.  
    #
    # Argument(s): 
    #  * G: The graph G being displayed
    #  * Gt: Abbreviated as Gtilde, or \tilde{G}, Gt is an induced subgraph to G (or self.Graph)
    #
    # Return(s): None
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def disp_isgraph(self, 
                     G : nx, 
                     Gt : nx): 
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
    
    def disp_graph_and_comp(self, G : nx):
        plt.subplot(1, 2, 1)
        nx.draw_networkx(G, width=2, node_size=800, font_size=12, font_color='white')
        plt.title(f"Graph $G$")

        plt.subplot(1, 2, 2)
        nx.draw_networkx(nx.complement(G), width=2, node_size=800, font_size=12, font_color='white')
        plt.title(f"Complement $G^c$")
        
        plt.show()

    def disp_rsf_colors(self, G : nx, F0 : list, F1 : list, R : list):
        node_list, node_colors = list(G.nodes), []

        for v in node_list: 
            if v in F0: node_colors.append('red')
            elif v in F1: node_colors.append('blue')
            else: node_colors.append('green')

        nx.draw_networkx(G, width=2, node_size=200, font_size=8, font_weight='bold', node_color=node_colors, font_color='white')

        legend_label = [
            Line2D([0], [0], marker='o', label=r'Neighbor to Simplicial Vertex', markerfacecolor='red', color='black'),
            Line2D([0], [0], marker='o', label=r'Simplicial Vertex', markerfacecolor='blue', color='black'),
            Line2D([0], [0], marker='o', label=r'Remaining Vertex', markerfacecolor='green', color='black')
        ]
        plt.legend(handles=legend_label, loc='lower left')

        plt.title(f"Final Graph Output")
        plt.show()

    def vertex_labels_P1(self, 
                     G : nx,
                     MIS_S : list,
                     key_idx : int):
        node_list, node_colors = list(G.nodes), []

        for v in node_list: 
            if v in MIS_S: node_colors.append('blue')
            else: node_colors.append('orange')                  # Remaining Vertices (Ignored)

        nx.draw_networkx(G, width=2, node_size=200, font_size=8, font_weight='bold', node_color=node_colors, font_color='white')

        legend_label = [
            Line2D([0], [0], marker='o', label=r'MIS Candidate Vertex', markerfacecolor='blue', color='black'),
            Line2D([0], [0], marker='o', label=r'Remaining Vertex', markerfacecolor='orange', color='black')
        ]
        plt.legend(handles=legend_label, loc='lower left')

        plt.title(f"Branch and Bound Scheme - Output (Index {key_idx})")
        plt.show()

    def vertex_labels_P2(self, 
                     G : nx,
                     F0 : list, 
                     F1 : list,
                     MIS_S : list,
                     key_idx : int):
        node_list, node_colors = list(G.nodes), []

        for v in node_list: 
            if v in F0: node_colors.append('red')
            elif v in F1: node_colors.append('blue')
            elif v in MIS_S: node_colors.append('green')
            else: node_colors.append('orange')                  # Remaining Vertices (Ignored)

        nx.draw_networkx(G, width=2, node_size=200, font_size=8, font_weight='bold', node_color=node_colors, font_color='white')

        legend_label = [
            Line2D([0], [0], marker='o', label=r'F0: Neighbor to Simplicial Vertex', markerfacecolor='red', color='black'),
            Line2D([0], [0], marker='o', label=r'F1: Simplicial Vertex', markerfacecolor='blue', color='black'),
            Line2D([0], [0], marker='o', label=r'MIS Candidate Vertex', markerfacecolor='green', color='black'),
            Line2D([0], [0], marker='o', label=r'Remaining Vertex', markerfacecolor='orange', color='black')
        ]
        plt.legend(handles=legend_label, loc='lower left')

        plt.title(f"RSF + Branch and Bound Scheme - Output (Index {key_idx})")
        plt.show()
