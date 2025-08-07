import numpy as np
import networkx as nx

class max_wc:
    def __init__(self, G : nx, W : dict): 
        self.graph = G

        temp_dict = {}
        for v in self.graph: temp_dict[v] = nx.degree(self.graph, v)
        
        self.W_color = {}
        self.W_node = W.copy() 
        self.C = {}
        self.color = {}

        self.Q = []
        self.Q_max = []

        # print(f"Sorted output: {R}\n")
        # print(f"W output: {W.items()}")

    def curr_sum_weight(self, min_k_w):
        curr_sum = 0
        for m in range(min_k_w): 
            print(f"self.C[{m}]: {self.C[m]}")
            for k in range(len(self.C[m])):
                curr_sum = curr_sum + self.W_node[self.C[m][k]]
                print(f"(m,k): ({m},{k}) - self.C[k][m]: {self.C[m][k]} - Weight: {self.W_node[self.C[m][k]]}")

        curr_Q_sum = 0
        for k in range(len(self.Q)):
            print(f"Here at k = {k}")
            curr_Q_sum += self.Q[k]

        curr_Qmax_sum = 0
        for k in range(len(self.Q_max)):
            curr_Qmax_sum += self.Q_max[k]

        print(f"\nStatus: {curr_sum <= curr_Qmax_sum - curr_Q_sum}\n")

        return curr_sum <= curr_Qmax_sum - curr_Q_sum

    def ColorSortWeight(self, R : list):
        maxno = 0
        self.C[0], self.C[1] = [], []
        self.W_color[0], self.W_color[1] = -1, -1

        for i in range(len(R)): 
            p = R[i]
            k = 0

            while list(set(self.C[k]).intersection(nx.neighbors(self.graph, p))) != []: k = k + 1

            if k > maxno: 
                maxno = k
                self.C[maxno + 1] = []
                self.W_color[maxno + 1] = -1

            self.W_color[k] = np.maximum(self.W_node[p], self.W_color[k])
            self.C[k].append(p)
            self.color[p] = k

        print(f"Color: {self.color}")
        print(f"Cliques: {self.C}")
        print(f"Clique Weights: {self.W_color}")
        print(f"Node Weights: {self.W_node}")
        print(f"maxno: {maxno}\n")

        min_k_w = 1
        while min_k_w < maxno and self.curr_sum_weight(min_k_w):
            min_k_w += 1

        print(f"R nodes: {R}\n")

        j = 0
        for i in range(len(R)-1):
            print(f"Color: {self.color}")
            print(f"R: {R}")
            # print(f"Index: {i} - Vertex: {R[i]}")
            print(f"Index: {i} - Vertex: {R[i]} - Color: {self.color[R[i]]}")
            if self.color[R[i]] < min_k_w:
                print(f"Vertex R[{j}]: {R[j]} | Vertex R[{i}]: {R[i]}")
                R[j] = R[i]
                j = j + 1

        if j > 0: self.color[R[j]] = -1

        print(f"\nR nodes: {R}")
        print(f"\nHere in the final line ... - min_k_w: {min_k_w}")
        print(f"Here with maxno = {maxno}\n")
        print(f"Color: {self.color}\n")

        for k in range(min_k_w, maxno, 1):
            ub_k = 0
            for n in range(1, k, 1):
                ub_k = ub_k + self.W_color[k]
            for i in range(len(self.color[k])-1):
                self.W_color[R[j]] = ub_k
                R[j] = self.color[k][i]
                j = j + 1
    
    def Expand(self, R : list):
        
        while R != []:
            p = R[len(R)-1]
            print(f"Output: {p}")

            weight_Q, weight_Qmax = 0, 0
            for v in self.Q: weight_Q = weight_Q + self.W_node[v]
            for v in self.Q_max: weight_Qmax = weight_Qmax + self.W_node[v]

            print(f"Q weight: {weight_Q}")
            print(f"Q_max weight: {weight_Qmax}\n")

            if weight_Q + self.color[p] > weight_Qmax:
                self.Q.append(p)
                Rp = list(set(R).intersection(list(nx.neighbors(self.graph, p))))
                
                if Rp != []:
                    
                    # Need to read more on Tlimit and T[lvl] ....
                    Rp_dict = {}
                    for v in Rp: Rp_dict[v] = nx.degree(self.graph, v)
                    Rp = list(dict(sorted(Rp_dict.items(), key = lambda item : item[1], reverse=True)))
                    
                    self.ColorSortWeight(Rp)
                    self.Expand(Rp)
                
                elif weight_Q > weight_Qmax:
                    self.Qmax = self.Q.copy()

                self.Q.remove(p)

            else: return

            R.remove(p)

