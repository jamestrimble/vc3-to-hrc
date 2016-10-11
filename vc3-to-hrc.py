import os
import sys

import graph

class HRC(object):
    def __init__(self, g, K):
        self.g = g
        self.idx_to_res = {}     # Dictionary res index -> name
        self.idx_to_hosp = {}    # Dictionary hosp index -> name
        self.num_couples = 0
        self.res_idx = 0
        self.hosp_idx = 0
        self.hosp_caps = {}  # Hosp name -> capacity
        self.rpref = {}    # A list of hosp names for each res
        self.hpref = {}    # A list of res names for each hosp
        
        m = g.get_m()
        n = g.n

        print self.vtx_to_edges(0)
        print self.vtx_to_edges(1)
        print self.vtx_to_edges(2)
        print self.vtx_to_edges(3)

        for j in range(m):
            self.add_couple("r_{}^1".format(j), "r_{}^2".format(j))
            self.add_couple("r_{}^3".format(j), "r_{}^4".format(j))

        for t in range(K):
            self.add_couple("f_{}^1".format(t), "f_{}^2".format(t))
            self.add_couple("f_{}^3".format(t), "f_{}^4".format(t))
            self.add_couple("f_{}^5".format(t), "f_{}^6".format(t))

        for t in range(n-K):
            self.add_couple("y_{}^1".format(t), "y_{}^2".format(t))
            self.add_couple("y_{}^3".format(t), "y_{}^4".format(t))
            self.add_couple("y_{}^5".format(t), "y_{}^6".format(t))

        for t in range(K):
            self.add_single("a_{}".format(t))
        for t in range(n-K):
            self.add_single("b_{}".format(t))

        for i in range(n):
            self.add_single("x_{}".format(i))

        # ALSO NEED:
        # p', q', x', d (dummy hospital for each vertex)


        for t in range(K):
            self.add_hosp("g_{}^1".format(t))
            self.add_hosp("g_{}^2".format(t))
            self.add_hosp("g_{}^3".format(t))

        for j in range(m):
            self.add_hosp("h_{}^1".format(j))
            self.add_hosp("h_{}^2".format(j))

        for t in range(K):
            self.add_hosp("p_{}^1".format(t))
        for t in range(n-K):
            self.add_hosp("q_{}^1".format(t))

        for t in range(n-K):
            self.add_hosp("z_{}^1".format(t))
            self.add_hosp("z_{}^2".format(t))
            self.add_hosp("z_{}^3".format(t))

    def vtx_to_edges(self, i):
        retval = []
        for j, e in enumerate(self.g.edges):
            if   e[0] == i: retval.append((0, j))
            elif e[1] == i: retval.append((1, j))
        return retval

    def add_couple(self, name1, name2):
        self.idx_to_res[self.res_idx] = name1
        self.idx_to_res[self.res_idx + 1] = name2
        self.res_idx += 2
        self.num_couples += 1
        self.rpref[name1] = []
        self.rpref[name2] = []

    def add_single(self, name):
        self.idx_to_res[self.res_idx] = name
        self.res_idx += 1
        self.rpref[name] = []

    def add_hosp(self, name, cap=1):
        self.idx_to_hosp[self.hosp_idx] = name
        self.hosp_idx += 1
        self.hosp_caps[name] = cap
        self.hpref[name] = []

    def add_rpref(self, rname, hname):
        self.rpref[rname].append(hname)

    def add_hpref(self, hname, rname):
        self.hpref[hname].append(rname)

    def show(self):
        pass

    def show_debug(self):
        print self.res_idx
        print self.hosp_idx
        print self.num_couples
        print sum(self.hosp_caps.values())
        for i in range(5):
            print
        for i in range(self.res_idx):
            rname = self.idx_to_res[i]
            sys.stdout.write(rname + ":")
            for hname in self.rpref[rname]:
                sys.stdout.write(" " + hname)
            sys.stdout.write(os.linesep)
        for i in range(self.hosp_idx):
            hname = self.idx_to_hosp[i]
            sys.stdout.write(hname + ":")
            for rname in self.hpref[hname]:
                sys.stdout.write(" " + rname)
            sys.stdout.write(os.linesep)

if __name__=="__main__":
    fname = sys.argv[1]
    K = int(sys.argv[2])
    g = graph.read(fname)
    hrc = HRC(g, K)
    hrc.show()
    hrc.show_debug()
