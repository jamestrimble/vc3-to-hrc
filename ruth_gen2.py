"""k copies of K4"""

import sys

def generate(k):
    edges = []
    print "{}\t{}".format(k*4, k*6)
    for i in range(k):
        for a, b in [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]:
            print "{}\t{}".format(a+4*i, b+4*i)

if __name__=="__main__":
    k = int(sys.argv[1])
    generate(k)
