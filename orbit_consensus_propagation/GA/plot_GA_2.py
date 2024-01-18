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

START_TIME = load_json(save_location+"/dataset.json")["timestamp"]

######### PART 2



STEP_SIZE = 30

group_set = 0   # 4/5/6/7/8 sats


consensus_times_all = csv_input(save_location+"/ga_results.csv")

while True:
    try:
        consensus_times = consensus_times_all[group_set]
    except:
        break

    DIS = 500
    group = []
    for i in range(2, len(consensus_times)):
        group.append(consensus_times[i])
    # group = consensus_times["Best"]["Set"]
    print(group)

    time_window = float(consensus_times[1])

    plt.subplots(figsize=(10,5))
    plt.plot([0, (time_window-START_TIME)],[DIS, DIS], c="black")
    for x, i in enumerate(group):
        for y, j in enumerate(group):
            if i != j and x < y:
                dis_data = np.asarray((csv_input(pos_data_location+"/"+str(i)+"_"+str(j)+".csv"))[0], dtype="float64")
                y = dis_data[0:int((time_window-START_TIME)/60)+1]
                print(dis_data)
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
    plt.savefig(save_location+"/GA_relative_distance_"+str(group_set+4)+".png")

    group_set += 1
