import sys

import graph

class HRC(object):
    def __init__(self, g):
        self.idx_to_res = {}     # Dictionary res index -> name
        self.idx_to_hosp = {}    # Dictionary hosp index -> name
        self.num_couples = 0
        self.res_idx = 0
        self.hosp_idx = 0
        self.hosp_caps = {}  # Hosp name -> capacity
        self.rpref = {}    # A list of hosp names for each res
        self.hpref = {}    # A list of res names for each hosp
        
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

    def add_hosp(self, name, cap):
        self.idx_to_hosp[self.hosp_idx] = name
        self.hosp_idx += 1
        self.hosp_caps.append(cap)
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

if __name__=="__main__":
    fname = sys.argv[1]
    k = int(sys.argv[2])
    g = graph.read(fname)
    hrc = HRC(g)
    hrc.show()
    hrc.show_debug()
