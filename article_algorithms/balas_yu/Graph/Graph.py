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

class Graph:
    def __init__(self, V : list, E : list): 
        self.V = V
        self.E = E
    
    def disp_all_v(self): print(self.V)
    def disp_all_e(self): print(self.E)

    def get_all_v(self): return self.V
    def get_all_e(self): return self.E
    
    def neighborhood(self, v : list): 
        N = []
        for u in self.V:
            if [u, v] in self.E: N.append(u)
            elif [v, u] in self.E: N.append(u)
        N.append(v)
        return N

    def non_neighborhood(self, v : int):
        N = self.neighborhood(v)
        not_N = [u for u in self.V if u not in N]
        return not_N

    def degree(self, v : int):
        return len(self.neighborhood(v))