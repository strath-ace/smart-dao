# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import numpy as np
import matplotlib.pyplot as plt
import os
from commons import *

########################## PARAMATERS #########################

file_name = "run_5683238_f"

SAVE_DIR = "data_icsmd_10day"

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
for F in history[50:]:
    T = F[F[:,0] != 1]
    T[:,1] = -T[:,1]
    min_times = []
    if len(T) == 0:
        F_li.append([])
        continue
    for i in range(int(np.amin(T[:,1])), int(np.amax(T[:,1]))+1):
        if np.any(T[:,1] == i):
            min_times.append( np.amin(T[T[:,1] == i][:,0]) )
    F_li.append(min_times)

_, indx = np.unique(np.asanyarray(F_li, dtype=object), return_index=True)
print("Solved in ", np.amax(indx), "generations")
print("Therefore took approximately", np.amax(indx)*400, "fitness evaluations")


