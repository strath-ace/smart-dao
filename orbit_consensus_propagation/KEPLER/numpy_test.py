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
from pytictoc import TicToc

# import blz
# # this stores the array in memory
# blz.barray(myarray) 
# # this stores the array on disk
# blz.barray(myarray, rootdir='arrays') 


######### INPUT PARAMS

# START_TIME = 1701448313 WIP --- IS NOW

config = load_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"))

TIMESTEP = config["STEP_SIZE"][0]
NUM_ITERATIONS = config["NUM_ITERATIONS"][0]

SAVE_DIR = "data_test"

STACK_SIZE = 400

DIS = 500*500

######### LOAD DATASETS

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_DIR)
if not os.path.exists(save_location):
    os.makedirs(save_location)
real_data = os.path.join(save_location, "real")
if not os.path.exists(real_data):
    os.makedirs(real_data)
    real_exist = False
else:
    real_exist = True
sim_data = os.path.join(save_location, "sim")
if not os.path.exists(sim_data):
    os.makedirs(sim_data)
    sim_exist = False
else:
    sim_exist = True
sim_results = os.path.join(save_location, "results")
if not os.path.exists(sim_results):
    os.makedirs(sim_results)

data_all_sats = load_json(save_location+"/sorted_sats.json")

START_TIME = load_json(save_location+"/dataset.json")["timestamp"]

iterations = np.linspace(START_TIME, START_TIME+(NUM_ITERATIONS*TIMESTEP), NUM_ITERATIONS)

######### GET POSITIONS OF SATELLITES IN DATASET
t = TicToc()


if not real_exist:
    all_sats = []
    c = 0
    for sat_data in data_all_sats:
        all_sats.append(ephem.readtle(sat_data["name"], sat_data["line1"], sat_data["line2"]))

    all_real_pos = []
    for order, sat in enumerate(all_sats):
        pos = []
        for i in iterations:
            timestep = datetime.fromtimestamp(i)
            sat.compute(timestep)
            pos.append(compute_pos(sat.sublong, sat.sublat, sat.elevation))
        all_real_pos.append(pos)
        if order % 10 == 0:
            print(order/len(all_sats))
    t.tic()
    np.save(real_data+"/big_file", all_real_pos)
    print("Real Data Save")
    t.toc()
   
if not sim_exist:
    fake_tle = {
        "name": "tester",
        "line1": "1 00900U 64063C   24005.89333868  .00000673  00000+0  69644-3 0  9994",
        "line2": "2 00900  90.1977   0.0000 0027154 181.7736 231.8234 13.74663288945296",
    }

    def checksum(into):
        sum = 0
        for n in into:
            li = [ord(x)-ord('0') for x in str(n) if x != '.']
            # print(li)
            for x in li:
                sum += x
        return (sum%10)

    inc_range = np.around(np.linspace(0,180,10), decimals=4)
    raan_range = np.around(np.linspace(0,360, 10), decimals=4)
    # ecc_range = np.around(np.logspace(0,7, 15, base=10), decimals=0)
    ecc_range = np.around(np.linspace(1,250000, 10), decimals=0)
    # print(ecc_range)
    argp_range = np.around(np.linspace(0,360, 10), decimals=4)
    anom_range = np.around(np.linspace(0,360, 10), decimals=4)
    motion_range = np.around(np.linspace(11.25, 16, 10), decimals=8)
    # MAX MEAN MOTION = 16, LEO MIN MOTION = 11.25 
    # print(motion_range)
    special_sat_data = []
    characters = {}
    c = 0
    stack_pos = []
    for i, inc in enumerate(inc_range):
        print(100*i/len(inc_range), "%")
        for raan in raan_range:
            for ecc in ecc_range:
                for argp in argp_range:
                    for anom in anom_range:
                        for motion in motion_range:
                            t2 = [2, 900, inc, raan, ecc, argp, anom, motion, 94529]
                            # print(fake_tle["line2"])
                            fake_tle["line2"] = ""
                            fake_tle["line2"] = fake_tle["line2"]+str(t2[0])+" "
                            fake_tle["line2"] = fake_tle["line2"]+str(t2[1]).zfill(5)+" "
                            fake_tle["line2"] = fake_tle["line2"]+f'{t2[2]:08.4f}'+" "
                            fake_tle["line2"] = fake_tle["line2"]+f'{t2[3]:08.4f}'+" "
                            fake_tle["line2"] = fake_tle["line2"]+f'{t2[4]:07.0f}'+" "
                            fake_tle["line2"] = fake_tle["line2"]+f'{t2[5]:08.4f}'+" "
                            fake_tle["line2"] = fake_tle["line2"]+f'{t2[6]:08.4f}'+" "
                            fake_tle["line2"] = fake_tle["line2"]+f'{t2[7]:010.8f}'
                            fake_tle["line2"] = fake_tle["line2"]+str(t2[8]).zfill(5)
                            fake_tle["line2"] = fake_tle["line2"]+str(checksum(t2))
                            # print(fake_tle["line2"])
                            
                            try:
                                sat = ephem.readtle(fake_tle["name"], fake_tle["line1"], fake_tle["line2"])
                                pos = []
                                # try:
                                for i in iterations:
                                    timestep = datetime.fromtimestamp(i)
                                    sat.compute(timestep)
                                    pos.append(compute_pos(sat.sublong, sat.sublat, sat.elevation))
                                    # SAVE POS in FILE
                                stack_pos.append(pos)
                                if len(stack_pos) >= STACK_SIZE:
                                    # csv_output(sim_data+"/"+str(c)+".csv", pos)
                                    np.savez_compressed(sim_data+"/"+str(c), stack_pos)
                                    stack_pos = []
                                    c += 1
                                characters.update({c: {"inc":inc, 
                                                    "raan":raan,
                                                    "ecc":ecc,
                                                    "argp":argp,
                                                    "anom":anom,
                                                    "motion":motion
                                                    }})
                                
                            except:
                                print(t2, "didnt work")

    np.savez_compressed(sim_data+"/"+str(c)+".csv", stack_pos)
    stack_pos = []
    c += 1

    save_json(save_location+"/kepler.json", characters)



# t.tic()
# all_real_pos = np.load(real_data+"/big_file.npy")
# print("Real Data Load")
# t.toc()

# partition = [[0, 300], [300, 600], [600, 900], [900, 1200], [1200, -1]]

# i = 0
# final_vals = []
# while True:
#     try:
#         stack_sim_pos = np.load(sim_data+"/"+str(i)+".npy")
#     except:
#         break
    
#     t.tic()
#     for j, sim_pos in enumerate(stack_sim_pos):
#         # print(all_real_pos[0])
#         # print(sim_pos)
#         # print("Restart")
#         summer = np.zeros(len(all_real_pos))
#         for part in partition:
#             c_real_pos = all_real_pos[np.logical_not(summer), part[0]:part[1]]-sim_pos[part[0]:part[1]]   # Expensive
#             # print(np.shape(c_real_pos))
#             norm = np.sum(np.square(c_real_pos), axis=2)    # 0.3 Expensive
#             # norm = np.linalg.norm(c_real_pos, axis=2)   # 0.4 Expensive
#             truth_table = norm<=DIS
#             summer[np.logical_not(summer)] = np.logical_or(np.any(truth_table, axis=1), summer[np.logical_not(summer)])
#         final_vals.append(np.sum(summer))


    #     # final_vals.append(summer)
    #     if j % 10 == 0:
    #         print(j / len(stack_sim_pos))
    # print("Stack", i, "done")
    # # (300 => 150s) 2 it/s
    # t.toc()
    # np.save(sim_results+"/"+str(i), final_vals)
    # i+=1