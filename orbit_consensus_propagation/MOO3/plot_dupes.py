# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import numpy as np
import matplotlib.pyplot as plt
import os
from commons import *

good_results = []

########################## PARAMATERS #########################

for kk in range(10):

    SAVE_DIR = "data_dupes/item_"+str(kk)

    # Get save location
    save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
    if not os.path.exists(save_location):
        raise Exception("Data File does not exist")

    # Get start time from save_location
    START_TIME = load_json(save_location+"/../dataset.json")["item_"+str(kk)]["start_time"]
    MAX_TIME = load_json(save_location+"/../dataset.json")["item_"+str(kk)]["max_time"]
    DIVIDED = MAX_TIME / (60*60)

    opt_location = os.path.join(save_location, "moo")
    if not os.path.exists(opt_location):
        raise Exception("Data File does not exist")
    opt_data = os.path.join(opt_location, "data")
    if not os.path.exists(opt_data):
        raise Exception("Data File does not exist")
    opt_results = os.path.join(save_location, "..", "results")
    if not os.path.exists(opt_results):
        os.makedirs(opt_results)


    obj = np.load(opt_data+"/run_f.npz")


    history = []
    for i in obj.files:
        history.append(np.array((obj[i])))

    obj.close()

    F = history[-1]

    F = np.unique(F, axis=0)
    print(F)

    F[:,0] = -F[:,0]
    F[:,1] = F[:,1]
    F[:,2] = -F[:,2]


    fig, ax1 = plt.subplots(figsize=(8,5))
    ax2 = ax1.twinx()

    ax1.set_xlabel("Number of Satellites in Consensus Subset")

    ax1.set_ylabel("Completness (0 -> 1)")
    ax1.set_ylim([0,1])

    ax2.set_ylabel("Consensus Time (Hours)")
    ax2.set_ylim([0,DIVIDED])
    # print(F[:,1])

    ax1.scatter(F[:, 2], F[:, 0], s=30, facecolors='none', edgecolors='red')
    ax2.scatter(F[:, 2], F[:, 1]*DIVIDED, s=30, facecolors='none', edgecolors='blue')

    ax1.yaxis.label.set_color("red")
    ax2.yaxis.label.set_color("blue")

    plt.title("Consensus Time and Completeness vs Number of Satellites in Subset")

    plt.savefig(opt_results+"/plot_"+str(kk)+".png")
    plt.clf()

    good_results.append(F[F[:,0] == 1])

# good_results = np.array(good_results)
for i in range(len(good_results)):
    if len(good_results[i]) > 1:
        print(good_results[i][:,2], good_results[i][:,1]*DIVIDED)
        plt.plot(good_results[i][:,2], good_results[i][:,1]*DIVIDED, label="item_"+str(i))
    else:
        print(good_results[i][:,2], good_results[i][:,1]*DIVIDED)
        plt.scatter(good_results[i][:,2], good_results[i][:,1]*DIVIDED,  label="item_"+str(i))

plt.xlabel("Number of Satellites in Consensus Subset")
plt.ylabel("Consensus Time (Hours)")
plt.legend()
plt.ylim([0,DIVIDED])
plt.title("Consensus Time vs Number of Satellites in Subset across all dupes")
plt.savefig(opt_results+"/plot_all_valid.png")
plt.clf()