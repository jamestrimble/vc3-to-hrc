import os
import pprint
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

        for j in range(m):
            self.add_couple("r_{}^1".format(j), "r_{}^2".format(j))
            self.add_couple("r_{}^3".format(j), "r_{}^4".format(j))
            for rsuper, hsuper in [(1,1), (2,2), (3,1), (4,2)]:
                self.add_rpref("r_{}^{}".format(j, rsuper), "h_{}^{}".format(j, hsuper))

        for t in range(K):
            self.add_couple("f_{}^1".format(t), "f_{}^2".format(t))
            self.add_couple("f_{}^3".format(t), "f_{}^4".format(t))
            self.add_couple("f_{}^5".format(t), "f_{}^6".format(t))
            for rsuper, hsuper in [(1,1), (2,2), (3,2), (4,3), (5,3), (6,1)]:
                self.add_rpref("f_{}^{}".format(t, rsuper), "g_{}^{}".format(t, hsuper))

        for t in range(n-K):
            self.add_couple("y_{}^1".format(t), "y_{}^2".format(t))
            self.add_couple("y_{}^3".format(t), "y_{}^4".format(t))
            self.add_couple("y_{}^5".format(t), "y_{}^6".format(t))
            for rsuper, hsuper in [(1,1), (2,2), (3,2), (4,3), (5,3), (6,1)]:
                self.add_rpref("y_{}^{}".format(t, rsuper), "z_{}^{}".format(t, hsuper))

        for t in range(K):
            self.add_single("a_{}".format(t))
            self.add_rpref("a_{}".format(t), "p_{}".format(t))
            self.add_rpref("a_{}".format(t), "g_{}^1".format(t))
        for t in range(n-K):
            self.add_single("b_{}".format(t))
            self.add_rpref("b_{}".format(t), "q_{}".format(t))
            self.add_rpref("b_{}".format(t), "z_{}^1".format(t))

        for i in range(n):
            # Change from model in paper: each x_i becomes a couple (x_i, x'_i)
            self.add_couple("x_{}".format(i), "x'_{}".format(i))

            for t in range(K):
                self.add_rpref("x_{}".format(i), "p_{}".format(t))
                self.add_rpref("x'_{}".format(i), "p'_{}".format(t))

            for pos_in_edge, vtx in self.vtx_to_edges(i):
                self.add_rpref("x_{}".format(i), "h_{}^{}".format(vtx, pos_in_edge))
            for j in range(3):
                self.add_rpref("x'_{}".format(i), "d_{}".format(i))

            for t in range(n-K):
                self.add_rpref("x_{}".format(i), "q_{}".format(t))
                self.add_rpref("x'_{}".format(i), "q'_{}".format(t))



        for t in range(K):
            for superscript in [1, 2, 3]:
                self.add_hosp("g_{}^{}".format(t, superscript))
            self.add_hpref("g_{}^1".format(t), "a_{}".format(t))
            for hsuper, rsuper in [(1,1), (1,6), (2,3), (2,2), (3,5), (3,4)]:
                self.add_hpref("g_{}^{}".format(t, hsuper), "f_{}^{}".format(t, rsuper))

        for j in range(m):
            self.add_hosp("h_{}^1".format(j))
            self.add_hosp("h_{}^2".format(j))
            self.add_hpref("h_{}^1".format(j), "r_{}^1".format(j))
            self.add_hpref("h_{}^1".format(j), "x_{}".format(self.g.edges[j][0]))
            self.add_hpref("h_{}^1".format(j), "r_{}^3".format(j))
            self.add_hpref("h_{}^2".format(j), "r_{}^4".format(j))
            self.add_hpref("h_{}^2".format(j), "x_{}".format(self.g.edges[j][1]))
            self.add_hpref("h_{}^2".format(j), "r_{}^2".format(j))

        for t in range(K):
            self.add_hosp("p_{}".format(t))
            self.add_hosp("p'_{}".format(t))
            for j in range(n):
                self.add_hpref("p_{}".format(t), "x_{}".format(j))
                self.add_hpref("p'_{}".format(t), "x'_{}".format(n-1-j))
            self.add_hpref("p_{}".format(t), "a_{}".format(t))

        for t in range(n-K):
            self.add_hosp("q_{}".format(t))
            self.add_hosp("q'_{}".format(t))
            for j in range(n):
                self.add_hpref("q_{}".format(t), "x_{}".format(j))
                self.add_hpref("q'_{}".format(t), "x'_{}".format(n-1-j))
            self.add_hpref("q_{}".format(t), "b_{}".format(t))

        for t in range(n-K):
            for superscript in [1, 2, 3]:
                self.add_hosp("z_{}^{}".format(t, superscript))
            self.add_hpref("z_{}^1".format(t), "b_{}".format(t))
            for hsuper, rsuper in [(1,1), (1,6), (2,3), (2,2), (3,5), (3,4)]:
                self.add_hpref("z_{}^{}".format(t, hsuper), "y_{}^{}".format(t, rsuper))

        for i in range(n):
            self.add_hosp("d_{}".format(i))
            self.add_hpref("d_{}".format(i), "x'_{}".format(i))
            

    def vtx_to_edges(self, i):
        retval = []
        for j, e in enumerate(self.g.edges):
            if   e[0] == i: retval.append((1, j))
            elif e[1] == i: retval.append((2, j))
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

    def show_instance_stats(self):
        """Prints the first few lines of the HRC instance"""
        print self.res_idx
        print self.hosp_idx
        print self.num_couples
        print sum(self.hosp_caps.values())
        for i in range(5):
            print

    def show(self):
        self.show_instance_stats()

        res_to_idx = {name: idx for idx, name in self.idx_to_res.iteritems()}
        hosp_to_idx = {name: idx for idx, name in self.idx_to_hosp.iteritems()}

        for i in range(self.res_idx):
            sys.stdout.write(str(i))
            rname = self.idx_to_res[i]
            for hname in self.rpref[rname]:
                sys.stdout.write("\t{}".format(hosp_to_idx[hname]))
            sys.stdout.write(os.linesep)
        for i in range(self.hosp_idx):
            hname = self.idx_to_hosp[i]
            sys.stdout.write("{}\t{}".format(i, self.hosp_caps[hname]))
            for rname in self.hpref[hname]:
                sys.stdout.write("\t".format(res_to_idx[rname]))
            sys.stdout.write(os.linesep)

    def show_debug(self):
        self.show_instance_stats()
        for i in range(self.res_idx):
            rname = self.idx_to_res[i]
            sys.stdout.write(rname + ":")
            for hname in self.rpref[rname]:
                sys.stdout.write(" " + hname)
                assert hname in self.hpref
            sys.stdout.write(os.linesep)
        for i in range(self.hosp_idx):
            hname = self.idx_to_hosp[i]
            sys.stdout.write(hname + ": ")
            sys.stdout.write("{}:".format(self.hosp_caps[hname]))
            for rname in self.hpref[hname]:
                sys.stdout.write(" " + rname)
                assert rname in self.rpref
            sys.stdout.write(os.linesep)

if __name__=="__main__":
    fname = sys.argv[1]
    K = int(sys.argv[2])
    g = graph.read(fname)
    hrc = HRC(g, K)
    if len(sys.argv) > 3:
        hrc.show_debug()
    else:
        hrc.show()
