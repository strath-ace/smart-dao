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

config = load_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.json"))

TIMESTEP = config["timestep"]
NUM_ITERATIONS = config["iterations"]
START_TIME = config["timestamp"]

######### LOAD DATASETS

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)
sim_data = os.path.join(save_location, "sim")
if not os.path.exists(sim_data):
    os.makedirs(sim_data)

iterations = np.linspace(START_TIME, START_TIME+(NUM_ITERATIONS*TIMESTEP), NUM_ITERATIONS)

############## Generate Sim sat tles

fake_tle = {
    "name": "tester",
    "line1": "1 00900U 64063C   24007.86057439  .00000704  00000+0  72958-3 0  9997",
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

num_in_grid = 3

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
all_pos = []
for i, inc in enumerate(inc_range):
    print(100*i/len(inc_range), "%")
    for raan in raan_range:
        for ecc in ecc_range:
            for argp in argp_range:
                for anom in anom_range:
                    for motion in motion_range:
                        title = str(inc)+"_"+str(raan)+"_"+str(ecc)+"_"+str(argp)+"_"+str(anom)+"_"+str(motion)
                        if not os.path.exists(sim_data+"/"+title):
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
                                # csv_output(save_location+"/"+str(c)+".csv", pos)
                                characters.update({c: {"inc":inc, 
                                                    "raan":raan,
                                                    "ecc":ecc,
                                                    "argp":argp,
                                                    "anom":anom,
                                                    "motion":motion
                                                    }})
                                # all_pos.append(pos)
                                
                                np.save(sim_data+"/"+title, pos)
                            except:
                                print("INC:", inc, "RAAN:", raan, "ECC:", ecc, "ARGP:", argp, "ANOM:", anom, "MOTION:", motion, "didnt work")
                        
# np.save(save_location+"/sim_pos", all_pos)
# save_json(save_location+"/sim_characteristics.json", characters)