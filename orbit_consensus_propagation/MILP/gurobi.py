from gurobipy import *
import matplotlib.pyplot as plt
import numpy as np

m = Model()
# v0 = m.addVar(vtype='B')
# v1 = m.addVar()
# m.addConstr(v0 - v1 <= 4)
# m.addConstr(v0 + v1 <= 5)
# m.addConstr(-0.25*v0 + v1 <= 1)

# n = 6*6*4
# shaped = np.zeros((6,6,4))
# X = m.addMVar(6,6,4)
# X = X.fromlist(shaped.tolist())

n= 6

X = np.empty((n,n,4)).tolist()
for i in range(n):
    for j in range(n):
        for k in range(4):
            X[i][j][k] = m.addVar(vtype="B")
X = np.array(X)


# Diagnols must be zero
for i in range(n):
    for k in range(4):
        m.addConstr(X[i,i,k] == 0)

S1 = np.sum(X[:,:,0])
S2 = np.sum(X[:,:,1])
S3 = np.sum(X[:,:,2])
S4 = np.sum(X[:,:,3])

# Totals
m.addConstr(S1 >= 3)
m.addConstr(S2 == S1*S1)
m.addConstr(S3 == S1*(S1-1))
m.addConstr(S4 == S1)


# Single Horizontal Line
# print(np.sum(X[:,:,0], axis=1) > 3)
# m.addConstr(np.sum() == 1)

# WIP ---- All in one line constrain, cant use np.any
m.addConstr(np.any(X[:,:,0]))

# for i in range(n):
    # m.addConstr(np.sum(X[i,:,0]) == S1)

# Tranpose phase 4
for i in range(n):
    for j in range(n):
        m.addConstr(X[j,i,0] == X[i,j,3])

m.update()
m.write("model.lp")
m.setObjective(np.sum(X), GRB.MINIMIZE)
m.params.outputflag = 0
m.optimize()


# Display X
X_view = np.zeros((4,n,n), dtype=int)
for i in range(n):
    for j in range(n):
        for k in range(4):
            X_view[k,i,j] = X[i][j][k].getAttr("x")


print(X_view)

# plt.imshow(X)
# plt.savefig("test.png")