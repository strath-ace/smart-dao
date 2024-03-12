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

T = np.load("data/converted/big.npz")["t"][:,10:20,10:20]

T = np.array(T, dtype=int)
# T = np.empty((1000,81,81), dtype=bool)





m = Model()

sh = np.shape(T)
max_time = 1000
print(sh)

c = 0
grid = np.zeros((max_time+1, 2*max_time+2), dtype=int)
grid = grid -1
for i in range(1,max_time+1):
    for j in range(max_time+1):
        # specific_perm.append((j, j+i))
        if j+i <= max_time:
            grid[j,j+i] = c
            c += 1
        if c > 500500:
            print(c)
print(c)
# print(grid)
# print(specific_perm[:1020])




combs = list(product(ran(sh[1]), ran(4), ran(max_time)))

x = np.empty((sh[1], 4, max_time), dtype=object)
for i in combs:
    x[i[0],i[1],i[2]] = m.addVar(vtype=GRB.BINARY)

y = np.empty(sh[1], dtype=object)
for i in ran(len(y)):
    y[i] = m.addVar(vtype=GRB.BINARY)

prim = np.empty(sh[1], dtype=object)
for i in ran(len(prim)):
    prim[i] = m.addVar(vtype=GRB.BINARY)

m.addConstr(np.sum(y) == 3) # Change this to MORE THAN 3
m.addConstr(np.sum(prim) == 1)

# Primary sat cannot be in y sats
for i in ran(sh[1]):
    m.addConstr(prim[i] + y[i] <= 1)

# Select based on y
for i in combs:
    m.addConstr(x[i[0],i[1],i[2]] <= prim[i[0]] + y[i[0]])

# Only 1 per phase per satellite
for i in ran(sh[1]):
    for p in ran(4):
        m.addConstr(np.sum(x[i,p,:]) == y[i]+prim[i])

# The next phase change has to be in a later timestep
for i in ran(sh[1]):
    for p in ran(4-1):
        for t in ran(max_time):
            m.addConstr(np.sum(x[i,p,:t]) >= x[i,p+1,t])
    for t in ran(max_time):
        m.addConstr(x[i,0,t]+x[i,1,t]+x[i,2,t]+x[i,3,t] <= 1)

#for j: for ta: y[j] * x[j,p,ta] * T[i,j,ta:t]

c = 0

ts = 0
s = 8
for t in ran(1,max_time):
    ta = grid[ts,t]
    for r in ran(sh[1]):
        adder = 0
        for s in ran(sh[1]):
            if s != r:
                adder += prim[s]*T[ta,s,r]
        m.addConstr(adder*x[r,0,t] == y[r]*x[r,0,t])
                # WIPIPWDIAHHBFALUH BFLOUHYIB
                # m.addConstr(x[r,0,t]*prim[s] <= T[ta,s,r])
                # m.addConstr(T[ta,s,r]*prim[s]+(1-prim[s])-(x[r,0,t]*y[r]) <= 1)
                # m.addConstr(y[r]*T[ta,s,r] >= x[r,0,t])
                # m.addConstr(x[r,0,t]*y[r] <= T[ta,s,r]*prim[s])

# Make first column 0
m.addConstr(np.sum(x[:,:,0]) == 0)







m.setObjective(np.sum(x), GRB.MAXIMIZE)
m.optimize()

x_view = np.empty(np.shape(x), dtype=int)
for i in combs:
    x_view[i[0],i[1],i[2]] = x[i[0],i[1],i[2]].getAttr("x")


y_view = np.empty(np.shape(y), dtype=int)
for i in ran(len(y_view)):
    y_view[i] = y[i].getAttr("x")

prim_view = np.empty(np.shape(prim), dtype=int)
for i in ran(len(prim_view)):
    prim_view[i] = prim[i].getAttr("x")

print()
print("#############")
print("Primary \t", prim_view)
print("Chosen sats \t", y_view)

x_view = x_view.swapaxes(0,1)
print("#############")
for i in range(4):
    print("Phase", i)
    print(x_view[i,:,:])

print("#############")
print("Summed together")
print(np.sum(np.array(np.sum(x_view, axis=0), dtype=bool),axis=1))