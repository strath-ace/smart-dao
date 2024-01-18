# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

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

USED_SATS_FILE = "sats_to_use_all.txt"
SAVE_DIR = "data_mixed"

START_TIME = reduce_sats(USED_SATS_FILE, SAVE_DIR)

######### LOAD DATASETS

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_DIR)
if not os.path.exists(save_location):
    os.makedirs(save_location)
big_data = os.path.join(save_location, "big")
if not os.path.exists(big_data):
    os.makedirs(big_data)
sim_data = os.path.join(save_location, "simulated")
if not os.path.exists(sim_data):
    os.makedirs(sim_data)

save_json(save_location+"/dataset.json", {"timestamp": START_TIME})