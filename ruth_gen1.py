import sys

def generate(n):
    edges = []
    for i in range(n):
        edges.append((i, (i+1)%n))
    for i in range(n/2):
        edges.append((i, i+n/2))

    print "{}\t{}".format(n, n*3/2)
    for e in sorted(edges):
        print "{}\t{}".format(*e)

if __name__=="__main__":
    n = int(sys.argv[1])
    if n % 2:
        sys.stderr.write("n must be even.\n")
        sys.exit(1)
    else:
        generate(n)
