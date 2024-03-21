from gurobipy import *
import matplotlib.pyplot as plt
import numpy as np
from pytictoc import TicToc
import os
from itertools import product
from numpy import arange as ran
import sys
np.set_printoptions(edgeitems=15)

ticcer = TicToc()

# subset_size = 

spots = [6,9,14,54,12]#, 1,2,3,4,5,7,8,10,11,12,13]
# spots = 10:20

T = np.load("data/converted/big_og.npz")["t"]

T = T[:,spots][:,:,spots]

T = np.array(T, dtype=int)

sh = np.shape(T)
max_time = 1000
print(sh)

m = Model()

combs = list(product(ran(sh[1]), ran(4), ran(max_time)))

c = 0
grid = np.zeros((max_time+1, 2*max_time+2), dtype=int)
grid = grid -1
for i in range(1,max_time+1):
    for j in range(max_time+1):
        # specific_perm.append((j, j+i))
        if j+i <= max_time:
            grid[j,j+i] = c
            c += 1
        else:
            break
print(c)

x2 = np.empty((sh[1], 4, max_time), dtype=object)
for i in combs:
    x2[i[0],i[1],i[2]] = m.addVar(vtype=GRB.BINARY)


t2 = 999
s = 1
r = 2

thing1 = ran(0,t2+1)
thing2 = (t2+1)*np.ones(t2+1, dtype=int)

m.update()

ticcer.tic()
adder = 0
for t1 in ran(t2+1):
    ta = grid[t1,t2+1]
    if T[ta,s,r]:
        adder += x2[s,0,t1]
ticcer.toc()
print(adder)

ticcer.tic()
ta = grid[thing1, thing2]
adder = np.sum(x2[s,0,T[ta,s,r]])
ticcer.toc()
print(adder)