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

from Graph.Graph import Graph                                                   ## Create an instance of G

class GenISGraph:
    def __init__(self): pass

    def gen_isgraph(self, G : Graph, Vt : list):
        Vt, V = sorted(Vt), G.get_all_v()
        Et, E = [], G.get_all_e()

        for u in Vt: 
            for v in Vt: 
                if u < v and [u, v] in E: Et.append([u, v])                     
        
        Gt = Graph(Vt, Et)
        return Gt