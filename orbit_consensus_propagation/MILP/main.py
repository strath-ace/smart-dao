# python -m pip install gurobipy
# python -m pip install gurobipy==11.0.0

from gurobipy import *
import matplotlib.pyplot as plt
import numpy as np
from pytictoc import TicToc
import os





n = 10

# Should be at least 4
min_sat = 4





T = np.load("./data/binary_1d.npy")

T = np.array(T, dtype=int)
# T[i,j,t]

indx = np.argsort(np.argsort(np.sum(np.sum(T,axis=2), axis=0)))
indx = indx[:n-4]

indx = np.append([6,9,14,54],indx)

T = np.load("./data/binary_10d.npy")
T = np.array(T, dtype=int)

T = T[indx][:,indx]

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

# T0 = np.empty(np.shape(T)).tolist()
# for j in range(n):
#     for i in range(n):
#         for t in range(np.shape(T)[2]):
#             print([i,j,t])
#             T0[i][j][t] = m.addVar()
#             bar1 = m.addVar()
#             m.addGenConstrOr(bar1, [T0[i][j][t] == T[i,j,t],  T0[i][j][t] == 999999])
#             m.addConstr(bar1 == 1)

# Phase 1

# t_list = []

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

# Phase 2

H2 = []
for j in range(n):
    temp = []
    for i in range(n):
        t_send = m.addVar()
        t_required = m.addVar()

        m.addConstr(t_send >= H1[i])
        m.addGenConstrMin(t_send, T[i,j])  # I think this executes before solve starts
        # t_list.append([i,j, t_send])
        m.addConstr(t_required == t_send * X[i,j,1])

        temp.append(t_required)

    t_final = m.addVar()
    m.addGenConstrMax(t_final, temp)
    H2.append(t_final)
H2 = np.array(H2)

m.update()

# t_list = np.array(t_list)
# for t in range(len(t_list)):
#     m.addGenConstrMin(t_list[t,2], T[t_list[t,0],t_list[t,1]])


# Phase 3

# H3 = []
# for j in range(n):
#     temp = []
#     for i in range(n):
#         new_var = m.addVar()
#         step_var = m.addVar()

#         m.addConstr(new_var >= H2[i])
#         m.addGenConstrMin(new_var, T[i,j])
#         m.addConstr(step_var == new_var * X[i,j,2])

#         temp.append(step_var)
#     h_var = m.addVar()
#     m.addGenConstrMax(h_var, temp, 0)
#     H3.append(h_var)
# H3 = np.array(H3)

# # Phase 4

# H4 = []
# for j in range(n):
#     temp = []
#     for i in range(n):
#         new_var = m.addVar()
#         step_var = m.addVar()
#         m.addGenConstrMin(new_var, T[i,j])
#         m.addConstr(step_var == new_var * X[i,j,3])
#         m.addConstr(step_var >= H3[j]*X[i,j,3])
#         temp.append(step_var)
#     h_var = m.addVar()
#     m.addGenConstrMax(h_var, temp, 0)
#     H4.append(h_var)
# H4 = np.array(H4)


consensus_time = m.addVar()
m.addGenConstrMax(consensus_time, H2, 0)

##################### OBJECTIVE AND SOLVE #####################

print("######## Solving")
ticcer.tic()

m.update()
m.write("model.lp")
m.setObjective(consensus_time, GRB.MINIMIZE)
m.params.outputflag = 0
# m.params.SolutionLimit = 1
# m.params.SolFiles("test.sol")
# m.params.Threads = 1
# m.params.Method = 0
m.params.MemLimit = 8
m.params.NodefileStart = 0.1
m.params.ResultFile = "results.sol"


m.optimize()

ticcer.toc()

##################### DISPLAY #####################

obj = m.getObjective()
print("H1")
# for i in range(n):
print(*[round(H1[i].getAttr("x")) for i in range(n)])
print("H2")
print(*[round(H2[i].getAttr("x")) for i in range(n)])

print()
print()
print("Objective:", obj.getValue())
print("Time:", obj.getValue()*30, "seconds")


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
