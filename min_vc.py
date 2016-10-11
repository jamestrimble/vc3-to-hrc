import sys

import graph

def covers_vertices(vv, g):
    for i, j in graph.edge_iter(g):
        if i not in vv and j not in vv:
            return False
    return True

def vc(g, i, vv):
    if len(vv) == i:
        return covers_vertices(vv, g)
    elif len(vv) == 0:
        for j in range(g.n):
            if vc(g, i, [j]): return True
    else:
        for j in range(vv[-1]+1, g.n):
            if  vc(g, i, vv+[j]): return True
    return False

def min_vc(g):
    for i in range(g.n+1):
        if vc(g, i, []):
            return i

if __name__=="__main__":
    fname = sys.argv[1]
    g = graph.read(fname)
    print min_vc(g)
