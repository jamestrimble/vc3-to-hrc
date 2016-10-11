import sys

class Graph(object):
    def __init__(self, n):
        self.n = n
        self.adj = [[] for i in range(n)]

    def add_edge(self, i, j):
        self.adj[i].append(j)
        self.adj[j].append(i)

    def show(self):
        for i in range(self.n):
            print self.adj[i]

def graph_edge_iter(g):
    for i, lst in enumerate(g.adj):
        for j in lst:
            yield i, j
            
def read_graph(fname):
    with open(fname, "r") as f:
        lines = [(int(x) for x in line.strip().split()) for line in f.readlines()]
    n, m = lines[0]
    g = Graph(n)
    edges =  lines[1:m+1]
    for e in edges:
        g.add_edge(*e)
    return g
    
def covers_vertices(vv, g):
    for i, j in graph_edge_iter(g):
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
    g = read_graph(fname)
    g.show()
    print min_vc(g)
