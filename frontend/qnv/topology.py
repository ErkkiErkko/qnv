import numpy as np

class Topology:
    def __init__(self, f):
        line = f.readline()
        self.n = int(line.split()[0])
        self.m = int(line.split()[1])
        self.p = np.zeros((self.n, self.n), dtype=float)
        self.q = [0.0] * self.n
        for i in range(0, self.m):
            line = f.readline()
            self.p[int(line.split()[0]) - 1][int(line.split()[1]) - 1] = float(line.split()[2])
            self.p[int(line.split()[1]) - 1][int(line.split()[0]) - 1] = float(line.split()[2])
        for i in range(0, self.n):
            line = f.readline()
            self.q[i] = float(line)
    
    def print(self):
        print(self.n)
        print(self.m)
        print(self.p)
        print(self.q)