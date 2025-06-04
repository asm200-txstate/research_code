from random import random

class GenGraph:
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: __init__ (Driver)
    #
    # Description: Constructor to the GenGraph class.
    #
    # Argument(s):
    #    * card_V: The number of vertices to the graph G
    #
    # Return(s): None
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def __init__(self, card_V=-1):
        if card_V <= -1:
            print("Invalid |V|, setting |V| = 10")
            card_V = 10
        
        print("Here in __init__() ...")
        self.card_V = card_V
        
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: gen_V
    #
    # Description: Generates the set of vertices, V, to the graph G.
    #
    # Argument(s): None
    #
    # Return(s): None
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def gen_V(self):
        V = []
        for v in range(self.card_V): V.append(v+1)
        
        print("Here in gen_V() ...")
        
        return V
        
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    # Method Name: gen_E
    #
    # Description: Generates the set of edges, E, to the graph G.
    #
    # Argument(s): None
    #
    # Return(s): None
    # ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****
    def gen_E(self):
        E = []
        
        for u in range(self.card_V):
            for v in range(self.card_V):
                add_uv = 1 if random() < 0.50 else 0
                if u < v and add_uv: E.append([u+1, v+1])
        
        print("Here in gen_E() ...")
        
        return E
