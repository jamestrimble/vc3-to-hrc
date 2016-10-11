import sys

import graph

if __name__=="__main__":
    fname = sys.argv[1]
    g = graph.read(fname)
    g.show()
    print graph.min_vc(g)
