# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import os
import json
import ephem
import numpy as np
import math
from datetime import datetime
from commons import *

######### INPUT PARAMS

# START_TIME = 1701448313 WIP --- IS NOW

config = load_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"))

TIMESTEP = config["STEP_SIZE"][0]
NUM_ITERATIONS = config["NUM_ITERATIONS"][0]

SAVE_DIR = "data_test"

######### LOAD DATASETS

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception(SAVE_DIR+" doesnt exist")
real_data = os.path.join(save_location, "real_sats")
if not os.path.exists(real_data):
    os.makedirs(real_data)

data_all_sats = load_json(save_location+"/sorted_sats.json")

START_TIME = load_json(save_location+"/dataset.json")["timestamp"]

iterations = np.linspace(START_TIME, START_TIME+(NUM_ITERATIONS*TIMESTEP), NUM_ITERATIONS)

######### GET POSITIONS OF SATELLITES IN DATASET

all_sats = []
for sat_data in data_all_sats:
    all_sats.append(ephem.readtle(sat_data["name"], sat_data["line1"], sat_data["line2"]))

for order, sat in enumerate(all_sats):
    pos = []
    if sat.n < 16 and sat.n > 11.25 and sat.e < 0.25:
        try:
            for i in iterations:
                timestep = datetime.fromtimestamp(i)
                sat.compute(timestep)
                pos.append(compute_pos(sat.sublong, sat.sublat, sat.elevation))

            # SAVE POS in FILE
            csv_output(real_data+"/"+str(order)+".csv", pos)
            print(100*order/len(all_sats),"% done - created", sat)
        except:
            pass
