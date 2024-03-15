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

spots = [6,9,14,54,12]
# spots = 10:20

T = np.load("data/converted/big.npz")["t"]

T = T[:,spots][:,:,spots]

T = np.array(T, dtype=int)
# T = np.empty((1000,81,81), dtype=bool)

num_sat = 4



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

x2 = np.empty((sh[1], 4, max_time), dtype=object)
for i in combs:
    x2[i[0],i[1],i[2]] = m.addVar(vtype=GRB.BINARY)

y = np.empty(sh[1], dtype=object)
for i in ran(len(y)):
    y[i] = m.addVar(vtype=GRB.BINARY)

prim = np.empty(sh[1], dtype=object)
for i in ran(len(prim)):
    prim[i] = m.addVar(vtype=GRB.BINARY)

m.addConstr(np.sum(y) == num_sat-1) # Change this to MORE THAN 3
m.addConstr(np.sum(prim) == 1)

# Primary sat cannot be in y sats
for i in ran(sh[1]):
    m.addConstr(prim[i] + y[i] <= 1)

# Select based on y
# for i in combs:
    # m.addConstr(x[i[0],i[1],i[2]] <= prim[i[0]] + y[i[0]])

# Only 1 per phase per satellite
for i in ran(sh[1]):
    for p in ran(4):
        m.addConstr(np.sum(x[i,p,:]) == y[i]+prim[i])

# The next phase change has to be in a later timestep
# for i in ran(sh[1]):
#     for p in ran(4-1):
#         for t in ran(max_time):
#             m.addConstr(np.sum(x[i,p,:t]) >= x[i,p+1,t])
#     for t in ran(max_time):
#         m.addConstr(x[i,0,t]+x[i,1,t]+x[i,2,t]+x[i,3,t] <= 1)

for i in ran(sh[1]):
    for p in ran(4):
        for t in ran(1,max_time+1):
            m.addConstr(x2[i,p,t-1] == np.sum(x[i,p,:t]))

# ########################### Set Primary ###########################
for s in ran(sh[1]):
    m.addConstr(prim[s] == x[s,0,0])

# ########################### Phase 0 ###########################
print("Start phase 0")
ticcer.tic()
ts = 0
for t in ran(1,max_time):
    ta = grid[ts,t]
    for r in ran(sh[1]):
        adder = 0
        for s in ran(sh[1]):
            if s != r:
                adder += prim[s]*T[ta,s,r]
        m.addConstr(adder >= x[r,0,t]*y[r])

ticcer.toc()
                
# ########################### Phase 1 ###########################
print("Start phase 1")
ticcer.tic()
for t2 in ran(1,max_time): 
    for r in ran(sh[1]):
        for s in ran(sh[1]):
            if s != r:
                adder = 0
                for t1 in ran(1,t2):
                    ta = grid[t1,t2]
                    adder += T[ta,s,r]*x2[s,0,t1]
                m.addConstr(x[r,1,t2]*y[s] <= adder)
ticcer.toc()                

# ########################### Phase 2 ###########################
print("Start phase 2")
ticcer.tic()
for t2 in ran(1,max_time): 
    for r in ran(sh[1]):
        for s in ran(sh[1]):
            if s != r:
                adder = 0
                for t1 in ran(1,t2):
                    ta = grid[t1,t2]
                    adder += T[ta,s,r]*x2[s,1,t1]
                m.addConstr(x[r,2,t2]*(y[s]+prim[s]) <= adder)
ticcer.toc()

# ########################### Phase 3 ###########################
print("Start phase 3")
ticcer.tic()
for t2 in ran(1,max_time): 
    for r in ran(sh[1]):
        for s in ran(sh[1]):
            if s != r:
                adder = 0
                for t1 in ran(1,t2):
                    ta = grid[t1,t2]
                    adder += T[ta,s,r]*x2[s,2,t1]
                m.addConstr(x[r,3,t2]*y[s] <= adder)
ticcer.toc()




# Correct people speak back
for t in ran(max_time):
    for r in ran(sh[1]):
        # Itself must be 1 in x2
        m.addConstr(x2[r,0,t] >= x[r,1,t])
        m.addConstr(x2[r,1,t] >= x[r,2,t])
        m.addConstr(x2[r,2,t] >= x[r,3,t])
        # Recieve from others must be 1 in x2
        for s in ran(sh[1]):
            m.addConstr(x2[s,0,t] >= x[r,1,t]*y[s])
            m.addConstr(x2[s,1,t] >= x[r,2,t]*(y[s]+prim[s]))
            m.addConstr(x2[s,2,t] >= x[r,3,t]*y[s])
                


outputs = np.empty(np.shape(x2)[1],dtype=object)
for i in range(np.shape(x2)[1]):
    outputs[i] = m.addVar(vtype=GRB.INTEGER)
    m.addConstr(outputs[i] == np.sum(x2[i,3,:]*prim[i]))


consensus_time = m.addVar()
m.addGenConstrMax(consensus_time, outputs.tolist())

m.params.SolutionLimit = 1
m.setObjective(consensus_time, GRB.MAXIMIZE)
m.optimize()

x_view = np.empty(np.shape(x), dtype=int)
for i in combs:
    x_view[i[0],i[1],i[2]] = x[i[0],i[1],i[2]].getAttr("x")

x2_view = np.empty(np.shape(x2), dtype=int)
for i in combs:
    x2_view[i[0],i[1],i[2]] = x2[i[0],i[1],i[2]].getAttr("x")

y_view = np.empty(np.shape(y), dtype=int)
for i in ran(len(y_view)):
    y_view[i] = y[i].getAttr("x")

prim_view = np.empty(np.shape(prim), dtype=int)
for i in ran(len(prim_view)):
    prim_view[i] = prim[i].getAttr("x")

obj = consensus_time.getAttr("x")
print()
print("#############")
print("Objective:", max_time-obj)
print("#############")
print("Primary \t", prim_view)
print("Chosen sats \t", y_view)

x_view = x_view.swapaxes(0,1)
x2_view = x2_view.swapaxes(0,1)
print("#############")
# print("Phase", 0)
# print(x_view[0,np.array(y_view+prim_view,dtype=bool),:])
for i in range(0,4):
    print("Phase", i)
    print(x_view[i,:,:])
    print(x2_view[i,:,:])

print("#############")
print("Summed together")
summed = (np.sum(np.array(np.sum(x_view, axis=2), dtype=bool), axis=0))
print(summed)
print("#############")
print("None of these should be zero:", np.sum(T[:1000,np.array(y_view,dtype=bool),np.array(prim_view,dtype=bool)], axis=0))
print("#############")
value = T[:400,np.array(y_view,dtype=bool),np.array(prim_view,dtype=bool)].tolist()
# for i, val in enumerate(value):
#     print(i, val)