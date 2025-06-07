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
    def __init__(self, V, E): 
        self.V = V
        self.E = E
    
    def disp_all_v(self): print(self.V)
    def disp_all_e(self): print(self.E)

    def get_all_v(self): return self.V
    def get_all_e(self): return self.E
    
    def neighborhood(self, v): 
        return []

    def non_neighborhood(self, v):
        return []
