import numpy as np

class Topology:
    def __init__(self, f):
        line = f.readline()
        self.n = int(line.split()[0])
        self.m = int(line.split()[1])
        self.p = np.zeros((self.n, self.n), dtype=float)
        self.q = [0.0] * self.n
        self.s = [-1] * self.n
        for i in range(0, self.m):
            line = f.readline()
            self.p[int(line.split()[0]) - 1][int(line.split()[1]) - 1] = float(line.split()[2])
            self.p[int(line.split()[1]) - 1][int(line.split()[0]) - 1] = float(line.split()[2])
        line = f.readline()
        _q = line.split()
        for i in range(0, self.n):
            self.q[i] = float(_q[i])
        line = f.readline()
        if not line:
            return
        _s = line.split()
        for i in range(0, self.n):
            self.s[i] = float(_s[i])
        
    
    def print(self):
        print(self.n)
        print(self.m)
        print(self.p)
        print(self.q)