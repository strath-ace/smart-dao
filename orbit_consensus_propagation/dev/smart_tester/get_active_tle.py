import os
import json
import ephem
import numpy as np
import math
from datetime import datetime
from py_lib.generic import *
from py_lib.get_less_sats import reduce_sats

######### INPUT PARAMS

USED_SATS_FILE = "sats_to_use_all.txt"
SAVE_DIR = "data"

START_TIME = reduce_sats(USED_SATS_FILE, SAVE_DIR)

######### LOAD DATASETS

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_DIR)
if not os.path.exists(save_location):
    os.makedirs(save_location)

save_json(save_location+"/dataset.json", {"timestamp": START_TIME})