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

import Graph.Graph as Graph
from .GenIS import GenIS
from .MISIP import MISIP

class BYBBStrat:
    def __init__(self, G : Graph):
        self.Graph = G
        V, E = self.Graph.get_all_v(), self.Graph.get_all_e()
        self.GIS = GenIS(self.Graph)
    
    def find_mis_helper(self): 
        pass
        
    def find_mis(self):
        S, U = self.GIS.gen_indset(), []
        print("Generated independent set S:", S)

        MIS_model = MISIP(self.Graph)
        MIS_model.optimize(S)
        
        # To be implemented later ...
        print(f"Optimal Solution: {MIS_model.opt_cost()}")
        MIS_model.opt_soln()
        
        # print(f"Optimal Set: {MIS_model.opt_soln()}")
