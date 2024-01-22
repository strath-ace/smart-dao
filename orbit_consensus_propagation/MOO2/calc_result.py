# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import numpy as np
import matplotlib.pyplot as plt
import os
from commons import *
from os import listdir
from os.path import isfile, join

########################## PARAMATERS #########################

SAVE_DIR = "data_icsmd_1day_v0"

######################### BUILD/FIND DIRECTORIES FOR DATA #########################

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("DATA FILE DOES NOT EXIST")
opt_location = os.path.join(save_location, "moo2")
if not os.path.exists(opt_location):
    raise Exception("NO DATA EXISTS TO PLOT")
opt_data = os.path.join(opt_location, "data")
if not os.path.exists(opt_data):
    raise Exception("NO DATA EXISTS TO PLOT")

onlyfiles = [f for f in listdir(opt_data) if isfile(join(opt_data, f))]

files_open = []
for i in range(len(onlyfiles)):
    if onlyfiles[i][-5] == "f":
        files_open.append(onlyfiles[i])


all_times = []
max_iter = []
for OPEN in files_open:
    obj = np.load(opt_data+"/"+OPEN)

    history = []
    for i in obj.files:
        history.append(np.array((obj[i])))

    obj.close()

    F = history[-1]

    F = np.unique(F, axis=0)

    F = F[F[:,0] != 1]

    F[:,0] = F[:,0]
    F[:,1] = -F[:,1]

    min_times = []
    num_sats = []
    for i in range(int(np.amin(F[:,1])), int(np.amax(F[:,1]))+1):
        min_times.append(np.amin(F[F[:,1] == i][:,0]))
        num_sats.append(i)

    for i in range(len(min_times)):
        if i >= len(all_times):
            all_times.append([])
        all_times[i].append(min_times[i])

    min_times = []
    num_sats = []
    F_li = []
    for F in history:
        F2 = F[F[:,0] != 1]
        F2[:,1] = -F2[:,1]
        min_times = []
        num_sats = []
        if len(F2) != 0:
            for i in range(int(np.amin(F2[:,1])), int(np.amax(F2[:,1]))+1):
                min_times.append(np.amin(F2[F2[:,1] == i][:,0]))
                num_sats.append(i)
        F_li.append(min_times)

    max_length = 0
    for i in range(len(F_li)):
        if max_length < len(F_li[i]):
            max_length = len(F_li[i])

    for i in range(len(F_li)):
        while len(F_li[i]) < max_length:
            F_li[i].append(0)

    _, indx = np.unique(np.asanyarray(F_li, dtype=float), axis=0, return_index=True)
    max_iter.append(np.amax(indx))

for x, times in enumerate(all_times):
    print(" ")
    print("#########", x+4 ,"#########")
    print(" ")
    uniques, counts = np.unique(times, return_counts=True)
    for i in range(len(uniques)):
        print(counts[i], "  ===  ", uniques[i])

print(" ")
print("######### Number of iterations to get to final result #########")
print(" ")
print(max_iter)
print("Average:", np.mean(max_iter))
print(" ")