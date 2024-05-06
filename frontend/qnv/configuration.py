from .topology import Topology

class DConfiguration:
    def __init__(self, mem: dict, ent, prob=1.0):
        self.mem = mem
        self.ent = ent
        self.prob = prob

    def assign(self, ident: str, value):
        self.mem[ident] = value
    
    def cr(self, ident: str, x, y, topo: Topology, pconf):
        if topo.p[x - 1][y - 1] < 1e-8 or self.ent[x - 1][y - 1] == topo.s[x - 1] or self.ent[x - 1][y - 1] == topo.s[y - 1]:
            self.mem[ident] = 0
            return
        new_mem = self.mem.copy()
        new_ent = self.ent.copy()
        new_mem[ident] = 1
        new_ent[x - 1][y - 1] = new_ent[x - 1][y - 1] + 1
        new_ent[y - 1][x - 1] = new_ent[x - 1][y - 1]
        pconf.dconfs.append(DConfiguration(new_mem, new_ent, self.prob * topo.p[x - 1][y - 1]))
        self.prob = self.prob * (1 - topo.p[x - 1][y - 1])
        self.mem[ident] = 0
    
    def sw(self, ident: str, x, y, z, topo: Topology, pconf):
        if self.ent[x - 1][z - 1] == 0 or self.ent[y - 1][z - 1] == 0:
            self.mem[ident] = 0
            return
        self.ent[x - 1][z - 1] = self.ent[x - 1][z - 1] - 1
        self.ent[z - 1][x - 1] = self.ent[x - 1][z - 1]
        self.ent[y - 1][z - 1] = self.ent[y - 1][z - 1] - 1
        self.ent[z - 1][y - 1] = self.ent[y - 1][z - 1]
        new_mem = self.mem.copy()
        new_ent = self.ent.copy()
        new_mem[ident] = 1
        new_ent[x - 1][y - 1] = new_ent[x - 1][y - 1] + 1
        new_ent[y - 1][x - 1] = new_ent[x - 1][y - 1]
        pconf.dconfs.append(DConfiguration(new_mem, new_ent, self.prob * topo.q[z - 1]))
        self.prob = self.prob * (1 - topo.q[z - 1])
        self.mem[ident] = 0
    
    def de(self, x, y, topo: Topology, pconf):
        if self.ent[x - 1][y - 1] == 0:
            return
        self.ent[x - 1][y - 1] = self.ent[x - 1][y - 1] - 1
        self.ent[y - 1][x - 1] = self.ent[x - 1][y - 1]

    def print(self):
        print(self.prob)
        print(self.mem)
        print(self.ent)


class PConfiguration:
    def __init__(self, dconfs: list):
        self.dconfs = dconfs

    def assign(self, ident: str, values: list):
        for i in range(0, len(self.dconfs)):
            self.dconfs[i].assign(ident, values[i])
    
    def cr(self, ident: str, values1: list, values2: list, topo: Topology):
        for i in range(0, len(values1)):
            self.dconfs[i].cr(ident, values1[i], values2[i], topo, self)

    def sw(self, ident: str, values1: list, values2: list, values3: list, topo: Topology):
        for i in range(0, len(values1)):
            self.dconfs[i].sw(ident, values1[i], values2[i], values3[i], topo, self)
    
    def de(self, values1: list, values2: list, topo: Topology):
        for i in range(0, len(values1)):
            self.dconfs[i].de(values1[i], values2[i], topo, self)

    def print(self):
        for dconf in self.dconfs:
            dconf.print()
            print('')