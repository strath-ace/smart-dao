# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import os
import ephem
import numpy as np
from datetime import datetime
from commons import *

######### INPUT PARAMS

TIMESTEP = 30
NUM_ITERATIONS = 2*1440

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

all_vals = []
all_vals_flat = []
distances = []
for order1, sat1 in enumerate(all_sats[:10]):
    pos1 = []
    for i in iterations:
        timestep = datetime.fromtimestamp(i)
        sat1.compute(timestep)
        pos1.append(compute_pos(sat1.sublong, sat1.sublat, sat1.elevation))
    temp = []
    temp_d = []
    for order2, sat2 in enumerate(all_sats[:10]):
        if order1 != order2:
            dis = []
            pos2 = []
            for i in iterations:
                timestep = datetime.fromtimestamp(i)
                sat2.compute(timestep)
                pos2.append(compute_pos(sat2.sublong, sat2.sublat, sat2.elevation))
            norm = np.sum(np.square(np.array(pos1)-np.array(pos2)), axis=1)
            temp_d.append(norm)
            exist = norm <= DIS*DIS
            output = iterations[exist]
            nan_list = np.empty(len(iterations)-len(output))
            nan_list[:] = np.nan
            output = np.append(output, nan_list)
            # print(output)
            temp.append(output)
            all_vals_flat.append(output)
        else:
            nan_list = np.empty(len(iterations))
            nan_list[:] = np.nan
            temp.append(nan_list)
            temp_d.append(nan_list)
            all_vals_flat.append(nan_list)
    temp = np.array(temp)
    temp_d = np.array(temp_d)
    distances.append(temp_d)
    all_vals.append(temp)
    print(100*order1/len(all_sats),"% done")

all_vals = np.array(all_vals)
all_vals_flat = np.array(all_vals_flat)

# print(np.shape(all_vals))
# print(np.shape(all_vals_flat))

all_vals[all_vals > 0] = all_vals[all_vals > 0] - START_TIME
all_vals_flat[all_vals_flat > 0] = all_vals_flat[all_vals_flat > 0] - START_TIME

np.save(save_location+"/all_combs", all_vals)
np.save(save_location+"/all_combs_flat", all_vals_flat)
np.save(save_location+"/all_distances", distances)
