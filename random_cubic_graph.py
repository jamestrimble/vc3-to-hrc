import random
import sys

def generate(n, K):
    """Print a random K-regular graph with n vertices"""

    x = 0
    while not try_to_generate(n, K):
        x += 1

def try_to_generate(n, K):
    candidate_edges = []
    for i in range(n):
        for j in range(n):
            if j > i:
                candidate_edges.append((i, j))

    chosen_edges = []

    vtx_degree = [0] * n

    while True:
        if len(chosen_edges) * 2 == n * K:
            print_graph(n, chosen_edges)
            return True
        if len(candidate_edges) == 0:
            return False
        i = random.randint(0, len(candidate_edges)-1)
        e = candidate_edges[i]
        chosen_edges.append(e)
        del candidate_edges[i]
        for v in e:
            vtx_degree[v] += 1
            if vtx_degree[v] == K:
                candidate_edges = [e for e in candidate_edges if v not in e]

def print_graph(n, edges):
    print "{}\t{}".format(n, len(edges))
    for e in sorted(edges):
        print "{}\t{}".format(*e)

if __name__=="__main__":
    n = int(sys.argv[1])
    K = 3 if len(sys.argv)==2 else int(sys.argv[2])
    if n * K % 2:
        sys.stderr.write("n*K is odd!")
        sys.exit(1)
    else:
        generate(n, K)
