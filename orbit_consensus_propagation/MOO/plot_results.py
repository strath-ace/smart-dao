# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import numpy as np
import matplotlib.pyplot as plt
import os
from commons import *

########################## PARAMATERS #########################

OPEN_FILE = "run_5583421_f.npz"

SAVE_DIR = "data_icsmd_1day_1sec"

######################### BUILD/FIND DIRECTORIES FOR DATA #########################

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("DATA FILE DOES NOT EXIST")
opt_location = os.path.join(save_location, "moo")
if not os.path.exists(opt_location):
    raise Exception("NO DATA EXISTS TO PLOT")
opt_data = os.path.join(opt_location, "data")
if not os.path.exists(opt_data):
    raise Exception("NO DATA EXISTS TO PLOT")
opt_results = os.path.join(opt_location, "results")
if not os.path.exists(opt_results):
    os.makedirs(opt_results)
opt_animation = os.path.join(opt_results, "opt_animation")
if not os.path.exists(opt_animation):
    os.makedirs(opt_animation)

dataset_file = load_json(save_location+"/dataset.json")
MASSIVE = dataset_file["max_time"]
MAX_TIME = MASSIVE / (60*60)

obj = np.load(opt_data+"/"+OPEN_FILE)

history = []
for i in obj.files:
    history.append(np.array((obj[i])))

obj.close()

F = history[-1]

F[:,0] = -F[:,0]
F[:,1] = F[:,1]
F[:,2] = -F[:,2]


fig, ax1 = plt.subplots(figsize=(8,5))
ax2 = ax1.twinx()

ax1.set_xlabel("Number of Satellites in Consensus Subset")

ax1.set_ylabel("Completness (0 -> 1)")
ax1.set_ylim([0,1])

ax2.set_ylabel("Consensus Time (Hours)")
ax2.set_ylim([0,MAX_TIME])


ax1.scatter(F[:, 2], F[:, 0], s=30, facecolors='none', edgecolors='red')
ax2.scatter(F[:, 2], F[:, 1]*MAX_TIME, s=30, facecolors='none', edgecolors='blue')

ax1.yaxis.label.set_color("red")
ax2.yaxis.label.set_color("blue")

plt.title("Consensus Time and Completeness vs Number of Satellites in Subset")

plt.savefig(opt_results+"/main_plot.png")

plt.clf()



# Start refined Graph

fig, ax1 = plt.subplots(figsize=(8,5))

idx = F[:,0] == 1

F2 = F[idx]

ax1.set_xlabel("Number of Satellites in Consensus, Subset")

ax1.scatter(F2[:, 2], F2[:, 1]*MAX_TIME, s=30, facecolors='none', edgecolors='blue')

ax1.set_ylabel("Consensus Time (Hours)")
ax1.set_ylim([0,MAX_TIME])
ax1.yaxis.label.set_color("blue")

plt.title("Refined view of consensus time for valid completeness")

plt.savefig(opt_results+"/refined_plot.png")
plt.clf()




# Print all history

for i, his in enumerate(history):

    F = his

    F[:,0] = -F[:,0]
    F[:,1] = F[:,1]
    F[:,2] = -F[:,2]

    fig, ax1 = plt.subplots(figsize=(8,5))
    ax2 = ax1.twinx()

    ax1.set_xlabel("Number of Satellites in Consensus Subset")
    ax1.set_xlim([3.6,82])

    ax1.set_ylabel("Completness (0 -> 1)")
    ax1.set_ylim([0,1])

    ax2.set_ylabel("Consensus Time (Hours)")
    ax2.set_ylim([0,MAX_TIME])


    ax1.scatter(F[:, 2], F[:, 0], s=30, facecolors='none', edgecolors='red')
    ax2.scatter(F[:, 2], F[:, 1]*MAX_TIME, s=30, facecolors='none', edgecolors='blue')

    ax1.yaxis.label.set_color("red")
    ax2.yaxis.label.set_color("blue")

    plt.title("Consensus Time and Completeness vs Number of Satellites in Subset Step: "+str(i))

    plt.savefig(opt_animation+"/"+str(i)+".png")

    plt.clf()
