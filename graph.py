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

def edge_iter(g):
    for i, lst in enumerate(g.adj):
        for j in lst:
            yield i, j
            
def read(fname):
    with open(fname, "r") as f:
        lines = [(int(x) for x in line.strip().split()) for line in f.readlines()]
    n, m = lines[0]
    g = Graph(n)
    edges =  lines[1:m+1]
    for e in edges:
        g.add_edge(*e)
    return g
    
