# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import os
import ephem
import numpy as np
from datetime import datetime
from commons import *

######### INPUT PARAMS

TIMESTEP = 1
NUM_ITERATIONS = 60*1440

SAVE_DIR = "data_icsmd_1day"

DIS = 500

######### LOAD DATASETS

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("Sat Data not setup, run get_active_tle.py first")
big_data = os.path.join(save_location, "close_times")
if not os.path.exists(big_data):
    os.makedirs(big_data)
dis_data = os.path.join(save_location, "relative_distance")
if not os.path.exists(dis_data):
    os.makedirs(dis_data)

data_all_sats = load_json(save_location+"/sorted_sats.json")

dataset = load_json(save_location+"/dataset.json")
START_TIME = dataset["timestamp"]

dataset.update({"max_time":TIMESTEP*NUM_ITERATIONS})

save_json(save_location+"/dataset.json", dataset)

iterations = np.round(np.linspace(START_TIME, START_TIME+(NUM_ITERATIONS*TIMESTEP), NUM_ITERATIONS))

######### GET POSITIONS OF SATELLITES IN DATASET

all_sats = []
for sat_data in data_all_sats:
    all_sats.append(ephem.readtle(sat_data["name"], sat_data["line1"], sat_data["line2"]))

bin_vals = []
for order1, sat1 in enumerate(all_sats):
    pos1 = []
    for i in iterations:
        timestep = datetime.fromtimestamp(i)
        sat1.compute(timestep)
        pos1.append(compute_pos(sat1.sublong, sat1.sublat, sat1.elevation))
    temp = []
    for order2, sat2 in enumerate(all_sats):
        if order1 != order2:
            pos2 = []
            for i in iterations:
                timestep = datetime.fromtimestamp(i)
                sat2.compute(timestep)
                pos2.append(compute_pos(sat2.sublong, sat2.sublat, sat2.elevation))
            norm = np.sum(np.square(np.array(pos1)-np.array(pos2)), axis=1)
            exist = norm <= DIS*DIS
            # print(exist)
            binar = np.zeros(len(iterations))
            binar[exist] = 1
            temp.append(binar)
        else:
            binar = np.zeros(len(iterations))
            temp.append(binar)
    bin_vals.append(temp)
    print(100*order1/len(all_sats),"% done")

bin_vals = np.array(bin_vals, dtype=bool)

np.save(save_location+"/binary", bin_vals)