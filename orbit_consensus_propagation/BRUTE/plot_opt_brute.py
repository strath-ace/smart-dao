# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import matplotlib.pyplot as plt
import numpy as np
import os
from commons import *

SAVE_DIR = "data_icsmd_1day"

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("DATA FILE DOES NOT EXIST")
pos_data_location = os.path.join(save_location, "relative_distance")
if not os.path.exists(save_location):
    raise Exception("Relative distance file does not exist")



consensus_times = load_json(save_location+"/brute_results.json")

START_TIME = load_json(save_location+"/dataset.json")["timestamp"]

TIME_DIVIDER = 60*60    # Seconds => Hours

best = []
rest = []
for i in range(len(consensus_times)):
    best.append((consensus_times[i]["Best"]))
    temp = []
    for time in consensus_times[i]["Rest"]:
        temp.append((time["ConsensusTime"]))
    # print(np.amin(temp))
    rest.append(temp)

fig, axs = plt.subplots(figsize=(10,15))

# plt.yscale("log")
max_val = 0
min_val = 99999999999999999999
for i in range(len(rest)):
    this_arr = (np.array(rest[i])-START_TIME)/TIME_DIVIDER
    violin = plt.violinplot(this_arr, [i+4], points=100, widths=0.8,
        showmeans=False, showextrema=False, showmedians=False)
    if max_val < np.amax(this_arr):
        max_val = np.amax(this_arr)
    if min_val > np.amin(this_arr):
        min_val = np.amin(this_arr)

print(min_val, "hrs => ", min_val*TIME_DIVIDER, "seconds")
print(max_val, "hrs => ", max_val*TIME_DIVIDER, "seconds")

plt.ylim([0, max_val*1.1])
plt.ylabel("Consensus Time (Hours)")
plt.xlabel("Number of satellites in subset")
#plt.yscale("log")




plt.savefig(save_location+"/brute_consensus_times.png")


plt.clf()





######### PART 2



STEP_SIZE = 60

group_set = 0   # 4/5/6/7/8 sats

while True:
    try:
        consensus_times = load_json(save_location+"/brute_results.json")[group_set]
    except:
        break

    DIS = 1000

    group = consensus_times["Best"]["Set"]

    time_window = consensus_times["Best"]["ConsensusTime"]

    plt.subplots(figsize=(10,5))
    plt.plot([0, (time_window-START_TIME)],[DIS, DIS], c="black")
    for x, i in enumerate(group):
        for y, j in enumerate(group):
            if i != j and x < y:
                dis_data = np.asarray((csv_input(pos_data_location+"/"+str(i)+"_"+str(j)+".csv"))[0], dtype="float64")
                y = dis_data[0:int((time_window-START_TIME)/60)+1]
                
                lab = str(i)+" vs "+str(j)
                # print(dis_data)
                plt.plot(y, label=lab)

    
    plt.xlabel("Time (mins)")
    plt.ylabel("Relative Distance between satellites")
    title = "Relative Distance for best subset with "+str(group_set+4)+" satellites"
    plt.title(title)

    plt.xlim([0,(time_window-START_TIME)/60])

    # plt.yscale("log")

    plt.legend()
    plt.savefig(save_location+"/relative_distance_"+str(group_set+4)+".png")

    group_set += 1
