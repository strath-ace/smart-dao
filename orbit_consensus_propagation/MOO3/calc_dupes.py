# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import numpy as np
import matplotlib.pyplot as plt
import os
from commons import *

good_results = []

########################## PARAMATERS #########################

for kk in range(10):

    SAVE_DIR = "data_dupes/item_"+str(kk)

    # Get save location
    save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
    if not os.path.exists(save_location):
        raise Exception("Data File does not exist")

    # Get start time from save_location
    START_TIME = load_json(save_location+"/../dataset.json")["item_"+str(kk)]["start_time"]
    MAX_TIME = load_json(save_location+"/../dataset.json")["item_"+str(kk)]["max_time"]
    DIVIDED = MAX_TIME / (60*60)

    opt_location = os.path.join(save_location, "moo")
    if not os.path.exists(opt_location):
        raise Exception("Data File does not exist")
    opt_data = os.path.join(opt_location, "data")
    if not os.path.exists(opt_data):
        raise Exception("Data File does not exist")
    opt_results = os.path.join(save_location, "..", "results")
    if not os.path.exists(opt_results):
        os.makedirs(opt_results)


    obj = np.load(opt_data+"/run_f.npz")


    history = []
    for i in obj.files:
        history.append(np.array((obj[i])))

    obj.close()

    F_li = []
    for F in history:
        F_li.append((F[F[:,0] == -1]).tolist())

    _, indx = np.unique(np.asanyarray(F_li, dtype=object), return_index=True)
    print("Solved in ", np.amax(indx), "generations")
    print("Therefore took approximately", np.amax(indx)*400, "fitness evaluations")


