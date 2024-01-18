import os
import json
import ephem
import numpy as np
import math
from datetime import datetime
from py_lib.generic import *
from py_lib.get_less_sats import reduce_sats

######### INPUT PARAMS

# START_TIME = 1701448313 WIP --- IS NOW

TIMESTEP = 60
NUM_ITERATIONS = 14400

SAVE_DIR = "data_icsmd_1day"

######### LOAD DATASETS

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("Sat Data not setup, run get_active_tle.py first")
big_data = os.path.join(save_location, "pos")
if not os.path.exists(big_data):
    os.makedirs(big_data)

data_all_sats = load_json(save_location+"/sorted_sats.json")

START_TIME = load_json(save_location+"/dataset.json")["timestamp"]

iterations = np.linspace(START_TIME, START_TIME+(NUM_ITERATIONS*TIMESTEP), NUM_ITERATIONS)

######### GET POSITIONS OF SATELLITES IN DATASET

all_sats = []
for sat_data in data_all_sats:
    all_sats.append(ephem.readtle(sat_data["name"], sat_data["line1"], sat_data["line2"]))

for order, sat in enumerate(all_sats):
    pos = []
    # if sat.n < 16 and sat.n > 11.25 and sat.e < 0.25:
    try:
        for i in iterations:
            timestep = datetime.fromtimestamp(i)
            sat.compute(timestep)
            pos.append(compute_pos(sat.sublong, sat.sublat, sat.elevation))

        # SAVE POS in FILE
        csv_output(big_data+"/"+str(order)+".csv", pos)
        print(100*order/len(all_sats),"% done - created", sat)
    except:
        pass
