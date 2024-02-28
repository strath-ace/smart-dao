# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import os
import ephem
import numpy as np
from datetime import datetime
from commons import *

######### INPUT PARAMS

config = load_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.json"))

TIMESTEP = config["timestep"]
NUM_ITERATIONS = config["iterations"]
START_TIME = config["timestamp"]

######### LOAD DATASETS

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)

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
for order, sat in enumerate(all_sats[:10]):
    pos = []
    for i in iterations:
        timestep = datetime.fromtimestamp(i)
        sat.compute(timestep)
        pos.append(compute_pos(sat.sublong, sat.sublat, sat.elevation))
        
    temp = np.array(temp)
    temp_d = np.array(temp_d)
    distances.append(temp_d)
    all_vals.append(temp)
    print(100*order1/len(all_sats),"% done")

