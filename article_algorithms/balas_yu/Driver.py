import sys
sys.dont_write_bytecode = True                                          ## Prevent __pycache__ from being generated

from GenGraph import GenGraph                                           ## Generate a graph G = (V,E)
from GraphPlot import GraphPlot                                         ## Plot a graph G = (V,E)

def main(argc, argv):
    RandG = GenGraph(int(argv[1]))
    V, E = RandG.gen_V(), RandG.gen_E()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Invalid argument count: {len(sys.argv)} - Try again ...")
        exit()
    
    # v_count = int(sys.argv[1])                                        ## Vertex Count
    # if v_count < 0:                                                   ## Check for valid |V|
    #     print("Invaid vertex count, setting |V| = 1")
    #     v_count = 1
    
    main(len(sys.argv), sys.argv)