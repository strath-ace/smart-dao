# python -m pip install gurobipy
# python -m pip install gurobipy==11.0.0

from gurobipy import *
import matplotlib.pyplot as plt
import numpy as np
from pytictoc import TicToc
import os





n = 15

# Should be at least 4
min_sat = 4





T = np.load("./data/binary_1d.npy")

T = np.array(T, dtype=int)
# T[i,j,t]

indx = np.argsort(np.argsort(np.sum(np.sum(T,axis=2), axis=0)))
indx = indx[:n-4]

# 6,9,14,54 give 4050 secs
# In list below this is 0,2,3,7
indx = np.append([6,7,9,14,17,18,19,54,55,56],indx)

T = np.load("./data/binary_1d.npy")
T = np.array(T, dtype=int)

T = T[indx][:,indx]

T = T[:,:,:200]

for t in range(np.shape(T)[2]):
    T[:,:,t][T[:,:,t] == 1] = t

T[T == 0] = 999999





m = Model()
print(" ")

# Create Clock
ticcer = TicToc()


##################### Generate Decision Variable X #####################

print("######## Generate Decision Variables")
ticcer.tic()

# Array X has size (n,n,4)s
X = np.empty((n,n,4)).tolist()
for k in range(4):
    for i in range(n):
        for j in range(n):
            X[i][j][k] = m.addVar(vtype="B")
X = np.array(X)
m.update()

# ------ Find Sums ------

S1 = np.sum(X[:,:,0])
S2 = np.sum(X[:,:,1])
S3 = np.sum(X[:,:,2])
S4 = np.sum(X[:,:,3])
ticcer.toc()


##################### SHAPE CONSTRAINTS #####################

print("######## General Constraints")
ticcer.tic()

# ------ Diagonals must be zero ------
for i in range(n):
    for k in range(4):
        m.addConstr(X[i,i,k] == 0)

# ------ Totals ------

m.addConstr(S1 >= min_sat-1)
m.addConstr(S2 == S1*S1)
m.addConstr(S3 == S1*(S1+1))
m.addConstr(S4 == S1)

ticcer.toc()

# ------ Single horizontal line in phase 1 ------

print("######## Phase 1 Constraints")
ticcer.tic()

# Create new variable for sum of each row in phase 1
row_sum_0 = []
for i in range(n):
    row_sum_0.append(m.addVar())
row_sum_0 = np.array(row_sum_0)
# Constrain the new variables to be sum of each row
for i in range(n):
    m.addConstr(row_sum_0[i] == np.sum(X[i,:,0]))

# SOS constraint only allows one non-zero element in array
m.addSOS(1, row_sum_0, wts=np.ones(n))
ticcer.toc()

# ------ Phase 2 Constraints ------

print("######## Phase 2 Constraints")
ticcer.tic()

# Rows should have S1 in each
for i in range(n):
    m.addConstr(S1*np.sum(X[:,i,0]) == np.sum(X[i,:,1]))

# Columns should have S1-1 in each (ignore primary)
for j in range(n):
    m.addConstr((S1-1)*np.sum(X[:,j,0]) == np.sum(X[:,j,1])*np.sum(X[:,j,0]))
    
# Primary column should have S1 in it
for i in range(n):
    for j in range(n):
        m.addConstr(X[i,j,0] == X[i,j,0]*X[j,i,1])
ticcer.toc()

# ------  Phase 3 ------
        
print("######## Phase 3 Constraints")
ticcer.tic()

for i in range(n):
    for j in range(n):
        m.addConstr(X[i,j,2] == (X[i,j,0]+ X[i,j,1]))
ticcer.toc()

# ------ Tranpose phase 4 ------
        
print("######## Phase 4 Constraints")
ticcer.tic()

for i in range(n):
    for j in range(n):
        m.addConstr(X[j,i,0] == X[i,j,3])
ticcer.toc()

##################### TIME CONSTRAINTS #####################

print("######## Time Constraints")

# Phase 1

print("######## Phase 1 Time Constraint")
ticcer.tic()
H1 = []
for j in range(n):
    temp = []
    for i in range(n):
        t_send = m.addVar()
        t_required = m.addVar()
        m.addGenConstrMin(t_send, T[i,j])
        # t_list.append([i,j, t_send])
        m.addConstr(t_required == t_send * X[i,j,0])
        temp.append(t_required)

    t_final = m.addVar()
    m.addGenConstrMax(t_final, temp)
    H1.append(t_final)
H1 = np.array(H1)
ticcer.toc()

eps = 0.0000001
M = 999999+eps

# Phase 2

print("######## Phase 2 Time Constraint")
ticcer.tic()
H2 = []
for j in range(n):
    temp = []
    for i in range(n):
        t_send = m.addVar()
        t_required = m.addVar()

        t0 = []
        for t in range(np.shape(T)[2]):
            b = m.addVar(vtype="B")
            m.addConstr(int(T[i,j,t]) >= H1[i] + eps - M * (1 - b))
            m.addConstr(int(T[i,j,t]) <= H1[i] + M * b)
            t_temp = m.addVar()
            m.addConstr((b == 1) >> (t_temp == T[i,j,t]))
            m.addConstr((b == 0) >> (t_temp == 999999))
            t0.append(t_temp)

        m.addGenConstrMin(t_send, t0)

        m.addConstr(t_required == t_send * X[i,j,1])

        temp.append(t_required)

    t_final = m.addVar()
    m.addGenConstrMax(t_final, temp)
    H2.append(t_final)
H2 = np.array(H2)
ticcer.toc()


m.update()


# Phase 3

print("######## Phase 3 Time Constraint")
ticcer.tic()
H3 = []
for j in range(n):
    temp = []
    for i in range(n):
        t_send = m.addVar()
        t_required = m.addVar()

        t0 = []
        for t in range(np.shape(T)[2]):
            b = m.addVar(vtype="B")
            m.addConstr(int(T[i,j,t]) >= H2[i] + eps - M * (1 - b))
            m.addConstr(int(T[i,j,t]) <= H2[i] + M * b)
            t_temp = m.addVar()
            m.addConstr((b == 1) >> (t_temp == T[i,j,t]))
            m.addConstr((b == 0) >> (t_temp == 999999))
            t0.append(t_temp)

        m.addGenConstrMin(t_send, t0)

        m.addConstr(t_required == t_send * X[i,j,2])

        temp.append(t_required)
    t_final = m.addVar()
    m.addGenConstrMax(t_final, temp)
    H3.append(t_final)
H3 = np.array(H3)
ticcer.toc()

# Phase 4

print("######## Phase 4 Time Constraint")
ticcer.tic()
H4 = []
for j in range(n):
    temp = []
    for i in range(n):
        t_send = m.addVar()
        t_required = m.addVar()

        t0 = []
        for t in range(np.shape(T)[2]):
            b = m.addVar(vtype="B")
            m.addConstr(int(T[i,j,t]) >= H3[i] + eps - M * (1 - b))
            m.addConstr(int(T[i,j,t]) <= H3[i] + M * b)
            t_temp = m.addVar()
            m.addConstr((b == 1) >> (t_temp == T[i,j,t]))
            m.addConstr((b == 0) >> (t_temp == 999999))
            t0.append(t_temp)

        m.addGenConstrMin(t_send, t0)

        m.addConstr(t_required == t_send * X[i,j,3])

        temp.append(t_required)

    t_final = m.addVar()
    m.addGenConstrMax(t_final, temp)
    H4.append(t_final)
H4 = np.array(H4)
ticcer.toc()

consensus_time = m.addVar()
m.addGenConstrMax(consensus_time, H4, 0)


##################### OBJECTIVE AND SOLVE #####################

print("######## Solving")

ticcer.tic()

m.update()
m.write("model.lp")
m.setObjective(consensus_time, GRB.MINIMIZE)
m.params.outputflag = 0
# m.params.SolutionLimit = 1
# m.params.SolFiles("test.sol")
m.params.Threads = 0
# m.params.Method = 0
m.params.MemLimit = 12
m.params.NodefileStart = 0.1
m.params.ResultFile = "results.sol"


m.optimize()

ticcer.toc()

##################### DISPLAY #####################

obj = m.getObjective()
print("H1")
print(*[round(H1[i].getAttr("x")) for i in range(n)])
print("H2")
print(*[round(H2[i].getAttr("x")) for i in range(n)])
print("H3")
print(*[round(H3[i].getAttr("x")) for i in range(n)])
print("H4")
print(*[round(H4[i].getAttr("x")) for i in range(n)])
# # print("Final Times")
# # print(*[round(conn_li[i].getAttr("x")) for i in range(n)])

print()
print()
print("Objective:", round(obj.getValue()))
print("Time:", round(obj.getValue())*30, "seconds")


X_view = np.zeros((4,n,n), dtype=int)
for i in range(n):
    for j in range(n):
        for k in range(4):
            X_view[k,i,j] = X[i][j][k].getAttr("x")

for i in range(np.shape(X_view)[1]):
    if np.sum(X_view[0,i,:]) > 0:
        print("Satellites Chosen:", i, *(np.arange(n)[X_view[0,i,:]==1]))

print()
print("Output X:")
print(X_view[0])







figure, axis = plt.subplots(2, 2, figsize=(10,10)) 

# For Sine Function 
axis[0, 0].imshow(X_view[0,:,:]) 
axis[0, 0].set_title("Pre-Prepare") 

# For Cosine Function 
axis[0, 1].imshow(X_view[1,:,:]) 
axis[0, 1].set_title("Prepare") 

# For Tangent Function 
axis[1, 0].imshow(X_view[2,:,:]) 
axis[1, 0].set_title("Commit") 

# For Tanh Function 
axis[1, 1].imshow(X_view[3,:,:]) 
axis[1, 1].set_title("Reply") 

plt.savefig("result.png")
