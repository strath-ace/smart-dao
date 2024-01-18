import ctypes as ctypes
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from datetime import datetime
from pytictoc import TicToc


n_var = 82

SAVE_DIR = "data_icsmd_100day"

MASSIVE = 60*1440*10*10
START_TIME = 1705065319



os.system("go build -buildmode=c-shared -o consensus.so consensus.go")

library = ctypes.cdll.LoadLibrary('./consensus.so')

conn1 = library.consensus_time1
conn1.argtypes = [ctypes.c_char_p]
conn1.restype = ctypes.c_void_p
conn2 = library.consensus_time2
conn2.argtypes = [ctypes.c_char_p]
conn2.restype = ctypes.c_void_p
conn3 = library.consensus_time3
conn3.argtypes = [ctypes.c_char_p]
conn3.restype = ctypes.c_void_p
conn4 = library.consensus_time4
conn4.argtypes = [ctypes.c_char_p]
conn4.restype = ctypes.c_void_p


def fit1(x):
    # print(genetics)
    document = {
        "ids": x
    }
    out = conn1(json.dumps(document).encode('utf-8'))
    if out in [1,2,3,4]:
        return MASSIVE
    return out-START_TIME

def fit2(x):
    # print(genetics)
    document = {
        "ids": x
    }
    out = conn2(json.dumps(document).encode('utf-8'))
    if out in [1,2,3,4]:
        return MASSIVE
    return out-START_TIME

def fit3(x):
    # print(genetics)
    document = {
        "ids": x
    }
    out = conn3(json.dumps(document).encode('utf-8'))
    if out in [1,2,3,4]:
        return MASSIVE
    return out-START_TIME

def fit4(x):
    # print(genetics)
    document = {
        "ids": x
    }
    out = conn4(json.dumps(document).encode('utf-8'))
    if out in [1,2,3,4]:
        return MASSIVE
    return out-START_TIME



##### 4

REBUILD = False

if REBUILD:
    future_set = []
    for i1 in range(n_var):
        print(i1/n_var)
        for i2 in range(i1, n_var):
            for i3 in range(i2, n_var):
                for i4 in range(i3, n_var):
                    future_set.append([i1,i2,i3,i4])

    working_set = []
    for i in range(len(future_set)):
        fit = fit4(future_set[i])
        if fit < MASSIVE:
            working_set.append([future_set[i], fit])
        if i % 100 == 0:
            print(i/len(future_set))

    working_set = np.array(working_set)
    # print(working_set[:,1])
    ind = np.argsort(working_set[:,1])
    # print(ind)
    working_set = np.array([working_set[i] for i in ind])
    np.save("data_fit4", working_set)

working_set = np.load("data_fit4.npy", allow_pickle=True)

num_list = []
for i in range(4,n_var+1):
    num_list.append(i)


num_to_produce = 100
all_all_saves = np.array([])

for j in range(num_to_produce):
    print(j)
    all_best_sets = []
    all_best_sets.append(working_set[j])

    best_set = working_set[j][0]
    # print(working_set[j][0])
    min_gene = 0
    while min_gene != MASSIVE and len(best_set) < n_var-1:
        min_gene = MASSIVE
        this_list = []
        for i in range(n_var):
            if i not in best_set:
                this_list.append([*best_set, i])

        for i in range(len(this_list)):
            fit = fit4(this_list[i])
            if fit < min_gene:
                min_gene = fit
                best_set = this_list[i]
        all_best_sets.append([best_set, min_gene])
        # print(best_set)

    all_best_sets = np.array(all_best_sets)

    all_all_saves = np.append(all_all_saves, all_best_sets)
    # print(np.shape(num_list[:len(all_best_sets)]), np.shape(all_best_sets[:,1]))
    plt.scatter(num_list[:len(all_best_sets)], all_best_sets[:,1]/(60*60), label=working_set[j][0])
    plt.xlabel("Number of satellites")
    plt.ylabel("Consensus Time (Hours)")
    # plt.legend()
    plt.savefig("test_fit4.png")

np.save("top_5_curves_fit4", all_all_saves)
# plt.ylim([0,MASSIVE*1.1/(60*60)])
