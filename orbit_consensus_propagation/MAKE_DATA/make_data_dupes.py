# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import os
import ephem
import numpy as np
from datetime import datetime
from commons import *
from progressbar import progressbar
from time import sleep

######### INPUT PARAMS

TIMESTEP = 30
NUM_ITERATIONS = 2*1440

SAVE_DIR = "data_dupes"

DIS = 500

JUMP = TIMESTEP*NUM_ITERATIONS

######### LOAD DATASETS

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("Sat Data not setup, run get_active_tle.py first")




data_all_sats = load_json(save_location+"/sorted_sats.json")

dataset = load_json(save_location+"/dataset.json")
START_TIME = dataset["timestamp"]

all_sats = []
for sat_data in data_all_sats:
    all_sats.append(ephem.readtle(sat_data["name"], sat_data["line1"], sat_data["line2"]))

for kk in range(10):

    NEW_START = START_TIME + (JUMP*kk)

    big_data = os.path.join(save_location, "item_"+str(kk))
    if not os.path.exists(big_data):
        os.makedirs(big_data)

    dataset.update({"item_"+str(kk): {"start_time": NEW_START, "max_time": JUMP}})

    iterations = np.round(np.linspace(NEW_START, NEW_START+(JUMP), NUM_ITERATIONS))

    ######### GET POSITIONS OF SATELLITES IN DATASET

    for order1 in progressbar(range(len(all_sats)), redirect_stdout=True, prefix="Building item "+str(kk)+": "):
        sat1 = all_sats[order1]
        pos1 = []
        for i in iterations:
            timestep = datetime.fromtimestamp(i)
            sat1.compute(timestep)
            pos1.append(compute_pos(sat1.sublong, sat1.sublat, sat1.elevation))
        for order2, sat2 in enumerate(all_sats):
            if order1 != order2:
                dis = []
                pos2 = []
                for i in iterations:
                    timestep = datetime.fromtimestamp(i)
                    sat2.compute(timestep)
                    pos2.append(compute_pos(sat2.sublong, sat2.sublat, sat2.elevation))
                norm = np.sum(np.square(np.array(pos1)-np.array(pos2)), axis=1)
                # print(np.shape(norm))
                # csv_output(dis_data+"/"+str(order1)+"_"+str(order2)+".csv", [np.sqrt(norm)])
                exist = norm <= DIS*DIS
                # print(exist)
                output = iterations[exist]
                # print(output)
                # print(output)
                if len(output) == 0:
                    csv_output(big_data+"/"+str(order1)+"_"+str(order2)+".csv", [[0]])
                else:
                    csv_output(big_data+"/"+str(order1)+"_"+str(order2)+".csv", [output])

save_json(save_location+"/dataset.json", dataset)