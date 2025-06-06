from Graph.Graph import Graph                                                   ## Create an instance of G

class GenISGraph:
    def __init__(self, G, U):
        self.Graph = G
        self.U = sorted(U)
    
    def gen_Et(self):
        Et = []
        E = self.Graph.get_allE()

        for u in self.U: 
            for v in self.U: 
                if u < v and [u, v] in E: Et.append([u, v])                     
        
        return Et