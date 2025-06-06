import Graph.Graph as Graph
from .GenIS import GenIS

class BYBBStrat:
    def __init__(self, G : Graph):
        self.Graph = G
        V, E = self.Graph.get_allV(), self.Graph.get_allE()

        self.GIS = GenIS(self.Graph)
        self.S = self.GIS.gen_IS()

        print("Generated independent set S: ", self.S)
    
    def step1(self):
        pass
