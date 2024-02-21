# python -m pip install gurobipy
# python -m pip install gurobipy==11.0.0

from gurobipy import *
import matplotlib.pyplot as plt
import numpy as np
from pytictoc import TicToc





n = 82

# Should be at least 4
min_sat = 4




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

##################### OBJECTIVE AND SOLVE #####################

print("######## Solving")
ticcer.tic()

m.update()
m.write("model.lp")
m.setObjective(np.sum(X), GRB.MINIMIZE)
m.params.outputflag = 0
# m.params.SolutionLimit = 1
# m.params.SolFiles("test.sol")
# m.params.Threads = 1
# m.params.Method = 0
m.params.MemLimit = 8
m.optimize()

ticcer.toc()

##################### DISPLAY #####################

X_view = np.zeros((4,n,n), dtype=int)
for i in range(n):
    for j in range(n):
        for k in range(4):
            X_view[k,i,j] = X[i][j][k].getAttr("x")


print(X_view)







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
