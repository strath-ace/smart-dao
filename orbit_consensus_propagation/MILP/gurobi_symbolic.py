from gurobipy import *
import matplotlib.pyplot as plt
import numpy as np
from pytictoc import TicToc
import os
from itertools import product as product_combs
from numpy import arange as ran
import sys
from sympy import *

init_printing(use_unicode=True)

np.set_printoptions(edgeitems=15)

ticcer = TicToc()

# subset_size = 

spots = [6,9,14,54,12]#, 1,2,3,4,5,7,8,10,11,12,13]
# spots = 10:20

T = np.load("data/converted/big_og.npz")["t"]

T = T[:,spots][:,:,spots]

T2 = np.array(T, dtype=int)
# T = np.empty((1000,81,81), dtype=bool)

num_sat = 4



m = Model()

sh = np.shape(T2)
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
        else:
            break
print(c)


T = np.empty((sh[0],sh[1],sh[2]),dtype=object)
for t in range(sh[0]):
    for s in range(sh[1]):
        for r in range(sh[1]):
            T[t,s,r] = m.addVar(vtype=GRB.BINARY)
            m.addConstr(T[t,s,r] == T2[t,s,r])

# print(grid)
# print(specific_perm[:1020])


combs = list(product_combs(ran(sh[1]), ran(4), ran(max_time)))

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


# Only 1 per phase per satellite except last phase where only primary has 1
for i in ran(sh[1]):
    for p in ran(3):
        m.addConstr(np.sum(x[i,p,:]) == y[i]+prim[i])
    m.addConstr(np.sum(x[i,3,:]) == prim[i])


# Change here if you dont want to communicate many on single timestep
for i in ran(sh[1]):
    for p in ran(4):
        for t in ran(max_time):
            m.addConstr(x2[i,p,t] == np.sum(x[i,p,:t+1]))

# ########################### Set Primary ###########################
for s in ran(sh[1]):
    m.addConstr(prim[s] == x[s,0,0])

m.update()

# m.update()
constr_list = []
var_list = []
# ########################### Phase 0 ###########################
print("Start phase 0")
ticcer.tic()
for t2 in ran(1,max_time): 
    for r in ran(sh[1]):
        adder = 0
        for s in ran(sh[1]):
            if s != r:
                ta = grid[0,t2+1]
                adder = T[ta,s,r]*prim[s]
                # m.addConstr(x[r,0,t2]*prim[s] <= adder)     # Working
                # adder2 = symbols("T_"+str(ta)+"_"+str(s)+"_"+str(r)) * symbols("prim")
                # print(adder2)
                # constr_list.append(symbols("x") <= adder2 + (1 - symbols("prim")))
                # var_list.append([r,0,t2,s])
                # print(constr_list)
                m.addConstr(x[r,0,t2] <= adder + (1-prim[s]))     # Tester
ticcer.toc()                

# T_500499_4_3 = symbols("T_500499_4_3")
# x_3_0_999 = symbols("x_3_0_999")
# prim_4 = symbols("prim_4")
# for i in range(len(constr_list)):
    # constr_list[i] = constr_list[i].subs(T_500499_4_3, T[500499,4,3])
    # print(str(constr_list[i].replace(x_3_0_999, x[3,0,999])))#, (prim_4, prim[4])])))




# ########################### Phase 1 ###########################
print("Start phase 1")
ticcer.tic()
for t2 in ran(1,max_time): 
    for r in ran(sh[1]):
        for s in ran(sh[1]):
            if s != r:
                adder = 0
                for t1 in ran(t2+1):
                    ta = grid[t1,t2+1]
                    adder += T[ta,s,r]*x2[s,0,t1]
                # m.addConstr(x[r,1,t2]*y[s] <= adder)    # Working
                m.addConstr(x[r,1,t2] <= adder + (1-y[s]))    # Tester
ticcer.toc()                

# ########################### Phase 2 ###########################
print("Start phase 2")
ticcer.tic()
for t2 in ran(1,max_time): 
    for r in ran(sh[1]):
        for s in ran(sh[1]):
            if s != r:
                adder = 0
                for t1 in ran(t2+1):
                    ta = grid[t1,t2+1]
                    adder += T[ta,s,r]*x2[s,1,t1]
                # m.addConstr(x[r,2,t2]*(y[s]+prim[s]) <= adder)    # Working
                m.addConstr(x[r,2,t2] <= adder + (1-(y[s]+prim[s])))    # Tester
ticcer.toc()

# ########################### Phase 3 ###########################
print("Start phase 3")
ticcer.tic()
for t2 in ran(1,max_time): 
    for r in ran(sh[1]):
        for s in ran(sh[1]):
            if s != r:
                adder = 0
                for t1 in ran(t2+1):
                    ta = grid[t1,t2+1]
                    adder += T[ta,s,r]*x2[s,2,t1]
                # m.addConstr(x[r,3,t2]*y[s] <= adder)    # Working
                m.addConstr(x[r,3,t2] <= adder+(1-y[s]))    # Tester
ticcer.toc()



# Correct people speak back
for t in ran(max_time):
    for r in ran(sh[1]):
        # Must complete previous phase before finishing next
        m.addConstr(x2[r,0,t] >= x[r,1,t])
        m.addConstr(x2[r,1,t] >= x[r,2,t])
        m.addConstr(x2[r,2,t] >= x[r,3,t])
        # The senders must have completed previous phase before sending
        for s in ran(sh[1]):
            # if s != r: # TESTER MIGHT REMOVE
            m.addConstr(x2[s,0,t]+(1-y[s]) >= x[r,1,t])
            m.addConstr(x2[s,1,t]+(1-(y[s]+prim[s])) >= x[r,2,t])
            m.addConstr(x2[s,2,t]+(1-y[s]) >= x[r,3,t])


# ########################### Objective and Execute Solver ###########################

# outputs = np.empty(np.shape(x2)[1],dtype=object)
# for i in range(np.shape(x2)[1]):
#     outputs[i] = np.sum(x2[i,3,:])*prim[i]
m.write("model.lp")
# m.params.SolutionLimit = 1
m.setObjective(np.sum(x2[:,3,:]), GRB.MAXIMIZE)
m.params.Threads = 0
ticcer.tic()
m.optimize()
print("##############")
print("Optimiser Solved")
ticcer.toc()

# ########################### Return Outputs ###########################

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

obj = m.getObjective()
obj = obj.getValue()

# ########################### Display Outputs ###########################

x_view = x_view.swapaxes(0,1)
x2_view = x2_view.swapaxes(0,1)

np.save("data/temp/x", x_view)
np.save("data/temp/x2", x2_view)

print("#############")
print("Objective:", max_time-obj)

print("#############")
print("Primary \t", prim_view)
print("Chosen sats \t", y_view)


print("#############")
print("Phase", 0)
print(x_view[0,:,:])
print(x2_view[0,:,:])
print("Phase", 1)
print(x_view[1,:,:])
print(x2_view[1,:,:])
print("Phase", 2)
print(x_view[2,:,:])
print(x2_view[2,:,:])
print("Phase", 3)
print(x_view[3,:,:])
print(x2_view[3,:,:])

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

m.close()