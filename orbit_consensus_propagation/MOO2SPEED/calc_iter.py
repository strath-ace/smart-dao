# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import numpy as np
import matplotlib.pyplot as plt
import os
from commons import *

########################## PARAMATERS #########################

file_name = "run_5705923_f"

SAVE_DIR = "data_icsmd_100day"

# Get save location
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("Data File does not exist")

# Get start time from save_location
START_TIME = load_json(save_location+"/dataset.json")["timestamp"]
MAX_TIME = load_json(save_location+"/dataset.json")["max_time"]
DIVIDED = MAX_TIME / (60*60)

opt_location = os.path.join(save_location, "moo2")
if not os.path.exists(opt_location):
    raise Exception("Data File does not exist")
opt_data = os.path.join(opt_location, "data")
if not os.path.exists(opt_data):
    raise Exception("Data File does not exist")
opt_results = os.path.join(save_location, "..", "results")
if not os.path.exists(opt_results):
    os.makedirs(opt_results)


obj = np.load(opt_data+"/"+file_name+".npz")

history = []
for i in obj.files:
    history.append(np.array((obj[i])))
obj.close()


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

# print(np.unique(np.asanyarray(F_li, dtype=float), axis=0))
_, indx = np.unique(np.asanyarray(F_li, dtype=float), axis=0, return_index=True)

# print(indx)
print("Solved in ", np.amax(indx), "generations")
print("Therefore took approximately", np.amax(indx)*400, "fitness evaluations")


