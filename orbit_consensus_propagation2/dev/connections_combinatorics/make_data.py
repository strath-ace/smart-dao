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

config = load_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"))

TIMESTEP = config["STEP_SIZE"][0]
NUM_ITERATIONS = config["NUM_ITERATIONS"][0]

REBUILD = True

USED_SATS_FILE = "sats_to_use_icsmd.txt"
SAVE_DIR = "data_icsmd"

START_TIME = reduce_sats(USED_SATS_FILE, SAVE_DIR)

######### LOAD DATASETS

iterations = np.linspace(START_TIME, START_TIME+(NUM_ITERATIONS*TIMESTEP), NUM_ITERATIONS)

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_DIR)
if not os.path.exists(save_location):
    os.makedirs(save_location)
big_data = os.path.join(save_location, "big")
if not os.path.exists(big_data):
    os.makedirs(big_data)

data_all_sats = load_json(save_location+"/sorted_sats.json")

save_json(save_location+"/dataset.json", {"timestamp": START_TIME})

######### GET POSITIONS OF SATELLITES IN DATASET

if REBUILD:
    all_sats = []
    for sat_data in data_all_sats:
        all_sats.append(ephem.readtle(sat_data["name"], sat_data["line1"], sat_data["line2"]))

    for order, sat in enumerate(all_sats):
        pos = []
        try:
            for i in iterations:
                timestep = datetime.fromtimestamp(i)
                sat.compute(timestep)
                pos.append(compute_pos(sat.sublong, sat.sublat, sat.elevation))

            # SAVE POS in FILE
            csv_output(big_data+"/"+str(order)+".csv", pos)
            print("Created", sat)
        except:
            pass

    print("Dataset generated")
