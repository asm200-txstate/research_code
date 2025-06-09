class OutputPrint:
    def __init__(self):
        self.label_width = 32
        self.timer = 0
        self.txt_file = None
    
    def print_top_line_break(self): print("\n" + "*" * 75 + "\n")

    def print_rec_level(self, level : int):
        print(f">>> {f'Current Recursion Level:':<{self.label_width}} Level {level}\n")

    def print_p1(self, V : list, S : list, U : list):
        print(f">>> {f'Current vertex set - V:':<{self.label_width}} {V}\n")
        print(f">>> {f'Candidate independent set S:':<{self.label_width}} {S}")
        print(f">>> {f'Candidate vertex subset - U:':<{self.label_width}} {U}\n")
    
    def print_p2(self, root : int, X_list : list, not_N : list): 
        print(f">>> {'Current VnU (Sorted by Degree):':<{self.label_width}} {X_list}")
        print(f">>> {f'Current Node {root} - not_N({root}) ':<{self.label_width}} {not_N}\n")
        
    def print_p3(self, idx, Xi_tilde, Vi):
        print(f">>> {f'Current X{idx}_tilde:':<{self.label_width}} {Xi_tilde}")
        print(f">>> {f'Current V{idx} | New V:':<{self.label_width}} {Vi}\n")
    
    def print_p4(self, I, X):
        print(f">>> {'Included Set (I):':<{self.label_width}} {I}")
        print(f">>> {'Excluded Set (X):':<{self.label_width}} {X}\n")

    def print_line_break(self): print("*" * 75 + "\n")