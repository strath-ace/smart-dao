from gurobipy import *
import matplotlib.pyplot as plt
import numpy as np
from pytictoc import TicToc
import os
from itertools import product
from numpy import arange as ran
import sys
np.set_printoptions(edgeitems=15)
from commons import *

ticcer = TicToc()


SAVE_DIR = "data_icsmd_1day"
how_many = 100
TIMESTEP = 30
NUM_ITERATIONS = 400

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("Sat Data not setup, run get_active_tle.py first")
many_data = os.path.join(save_location, "many")
if not os.path.exists(many_data):
    os.makedirs(many_data)

dataset = load_json(save_location+"/dataset.json")
START_TIME = dataset["timestamp"]

START_TIME += how_many*NUM_ITERATIONS*TIMESTEP + NUM_ITERATIONS*TIMESTEP

start_set = np.array(np.linspace(START_TIME, START_TIME+how_many*NUM_ITERATIONS*TIMESTEP, how_many), dtype=int)




# subset_size = 

# spots = [1,6,9,14]#,54, 1,2,3,4,5,7,8,10,11,12,13]
# spots = 10:20

spots = [5, 13, 50,  8, 12, 25,  9, 36, 34, 29, 47, 30, 38, 23,  7, 17, 45, 71, 69, 75]
spots = [5, 13, 50,  8, 67, 66, 52, 54, 12, 36, 25,  9, 34, 29, 30,  7, 79, 71, 23, 47, 17, 69, 38, 80, 45, 70, 42,  2, 75, 24]

for start in start_set:
    T = np.load("data/many_converted/conv_"+str(start)+".npz")["t"]

    T_sum = np.sum(T,axis=(0,1))

    T = T[:,spots][:,:,spots]
    # T = T[:,:20][:,:,:20]

    T = np.array(T, dtype=int)
    # T = np.empty((1000,81,81), dtype=bool)

    num_sat = 4



    m = Model()

    sh = np.shape(T)
    max_time = 400
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
    # print(c)
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

    # ########################### Phase 0 ###########################
    print("Start phase 0")
    # ticcer.tic()
    for t2 in ran(1,max_time): 
        for r in ran(sh[1]):
            for s in ran(sh[1]):
                if s != r:
                    ta = grid[0,t2+1]
                    if T[ta,s,r]:
                        # adder = prim[s]
                        m.addConstr(x[r,0,t2] <= 1)
                    else:
                        # adder = 0
                        m.addConstr(x[r,0,t2] <= 1 - prim[s])
                    # m.addConstr(x[r,0,t2]*prim[s] <= adder)     # Working
                    # m.addConstr(x[r,0,t2] <= adder + (1-prim[s]))     # Tester
    # ticcer.toc()                
                    
    # ########################### Phase 1 ###########################
    print("Start phase 1")
    # ticcer.tic()
    for t2 in ran(1,max_time): 
        for r in ran(sh[1]):
            for s in ran(sh[1]):
                if s != r:
                    adder = 0
                    for t1 in ran(t2+1):
                        ta = grid[t1,t2+1]
                        if T[ta,s,r]:
                            adder += x2[s,0,t1]
                    # m.addConstr(x[r,1,t2]*y[s] <= adder)    # Working
                    m.addConstr(x[r,1,t2] <= adder + (1-y[s]))    # Tester
    # ticcer.toc()                

    # ########################### Phase 2 ###########################
    print("Start phase 2")
    # ticcer.tic()
    for t2 in ran(1,max_time): 
        for r in ran(sh[1]):
            for s in ran(sh[1]):
                if s != r:
                    adder = 0
                    for t1 in ran(t2+1):
                        ta = grid[t1,t2+1]
                        if T[ta,s,r]:
                            adder += x2[s,1,t1]
                    # m.addConstr(x[r,2,t2]*(y[s]+prim[s]) <= adder)    # Working
                    m.addConstr(x[r,2,t2] <= adder + (1-(y[s]+prim[s])))    # Tester
    # ticcer.toc()

    # ########################### Phase 3 ###########################
    print("Start phase 3")
    # ticcer.tic()
    for t2 in ran(1,max_time): 
        for r in ran(sh[1]):
            for s in ran(sh[1]):
                if s != r:
                    adder = 0
                    for t1 in ran(t2+1):
                        ta = grid[t1,t2+1]
                        if T[ta,s,r]:
                            adder += x2[s,2,t1]
                    # m.addConstr(x[r,3,t2]*y[s] <= adder)    # Working
                    m.addConstr(x[r,3,t2] <= adder+(1-y[s]))    # Tester
    # ticcer.toc()



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
    m.params.Presolve = 0
    # m.params.SolutionLimit = 1
    m.setObjective(np.sum(x2[:,3,:]), GRB.MAXIMIZE)
    m.params.Threads = 10
    m.params.Method = 1
    m.params.NodefileStart = 0.5
    m.params.PreSparsify = True
    ticcer.tic()
    try:
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

        np.save("data/many_out/x_other_"+str(start), x_view)
        np.save("data/many_out/x2_other_"+str(start), x2_view)

    except:
        pass

    m.close()