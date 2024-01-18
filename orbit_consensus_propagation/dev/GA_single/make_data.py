import ctypes
import os
import json
import ephem
import numpy as np
import math
from datetime import datetime
from generic import *

######### INPUT PARAMS

START_TIME = 1701448313
TIMESTEP = 60
NUM_ITERATIONS = 100*60

REBUILD = True


######### LOAD DATASETS

iterations = np.linspace(START_TIME, START_TIME+(NUM_ITERATIONS*TIMESTEP), NUM_ITERATIONS)


save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)
big_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "big")
if not os.path.exists(big_data):
    os.makedirs(big_data)

data_all_sats = load_json(save_location+"/sorted_sats.json")

######### GET POSITIONS OF SATELLITES IN DATASET

if REBUILD:
    all_sats = []
    for sat_data in data_all_sats:
        all_sats.append(ephem.readtle(sat_data["name"], sat_data["line1"], sat_data["line2"]))

    for order, sat in enumerate(all_sats):
        pos = []
        for i in iterations:
            timestep = datetime.fromtimestamp(i)
            sat.compute(timestep)
            pos.append(compute_pos(sat.sublong, sat.sublat, sat.elevation))

        # SAVE POS in FILE
        csv_output(big_data+"/"+str(order)+".csv", pos)

    print("Dataset generated")
