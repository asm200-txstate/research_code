import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx

class GraphPlot:
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: __init__ (Driver)
    #
    # Description: ...
    #
    # Argument(s):
    #    * ...
    #    * ...
    #
    # Return(s): ...
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def __init__(self, V, E): 
        self.V = V
        self.E = E

        G = nx.Graph()
        G.add_nodes_from(self.V)
        G.add_edges_from(self.E)

    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: disp_G
    #
    # Description: ...
    #
    # Argument(s):
    #    * ...
    #    * ...
    #
    # Return(s): ...
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def disp_G(self): pass

    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: disp_ISG
    #
    # Description: ...
    #
    # Argument(s):
    #    * ...
    #    * ...
    #
    # Return(s): ...
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def disp_ISG(self): pass

# class GraphVisual:
#     ## Name: __init__ (Driver)
#     ## Description: Initializes the set of vertices and edges, denoted
#     ##              V and E, respectively, for the graph G = (V,E).
#     ## Argument(s):
#     ## * V: Set of vertices to G.
#     ## * E: Set of edges to G.
#     ## Return(s): None
#     def __init__(self,V,E):
#         self.V = V
#         self.E = E

#     ## Name: display_graph
#     ## Description: Displays the randomized graph to the terminal.
#     ## Argument(s): None
#     ## Return(s): None
#     def display(self):
#         G = nx.Graph()
#         G.add_nodes_from(self.V)
#         G.add_edges_from(self.E)
        
#         pos = nx.circular_layout(G, 2)
        
#         nx.draw_networkx(G, pos, width=2, node_size=800, font_size=12, font_color='white')
#         plt.title(f"Induced Subgraph for $K_{{{len(self.V)}}}$")
#         plt.show()
    
#     ## Name: disp_ind_subgraph
#     ## Description: Displays the induced subgraph, G[U] := (U,\tilde{E}), within the graph G=(V,E).
#     ## Argument(s): None
#     ## Return(s): None
#     def disp_ind_subgraph(self,U,Et):
#         G = nx.Graph()
#         G.add_nodes_from(self.V)
#         G.add_edges_from(self.E)
        
#         pos = nx.circular_layout(G, 2)
        
#         extras = {"node_size" : 800}                                ## Supplemental details to networkx
        
#         nx.draw_networkx(G, pos, width=3, font_size=18, font_color='white', **extras)
        
#         ## Node Updates
#         nx.draw_networkx_nodes(G, pos, nodelist=U, node_color="tab:red", **extras)
        
#         ## Edge Updates
#         nx.draw_networkx_edges(G, pos, width=3, edgelist=Et, edge_color="tab:red", **extras)
        
#         ## Formats the legend in plot
#         legend_elements = [
#             Line2D([0], [0], marker='o', label='G = (V, E)', markerfacecolor='tab:blue'),
#             Line2D([0], [0], marker='o', label=r'$\tilde{G} = (U, \tilde{E})$', markerfacecolor='tab:red', color='tab:red')
#         ]

#         plt.legend(handles=legend_elements, loc='upper right')

#         plt.title(r"Induced Subgraph Plot")
#         plt.show()