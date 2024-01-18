import ctypes
import os
import json
import ephem
import numpy as np
import math
from datetime import datetime
from py_lib.generic import *
from py_lib.get_less_sats import reduce_sats
from pytictoc import TicToc
import asyncio
import scipy.optimize as opt

######### INPUT PARAMS

TIMESTEP = 60
NUM_ITERATIONS = 1440

SAVE_DIR = "data"

STACK_SIZE = 100

DIS = 1000*1000

######### LOAD DATASETS

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_DIR)
if not os.path.exists(save_location):
    os.makedirs(save_location)
# real_data = os.path.join(save_location, "real.npy")
# if not os.path.exists(real_data):
#     real_exist = False
# else:
#     real_exist = True
big_data_loc = os.path.join(save_location, "big")
if not os.path.exists(big_data_loc):
    os.makedirs(big_data_loc)
# sim_results = os.path.join(save_location, "results")
# if not os.path.exists(sim_results):
#     os.makedirs(sim_results)

data_all_sats = load_json(save_location+"/sorted_sats.json")

START_TIME = load_json(save_location+"/dataset.json")["timestamp"]
END_TIME = START_TIME+(NUM_ITERATIONS*TIMESTEP)

iterations = np.linspace(START_TIME, START_TIME+(NUM_ITERATIONS*TIMESTEP), NUM_ITERATIONS)

######### GET POSITIONS OF SATELLITES IN DATASET
toccer = TicToc()



print("Generating Real Satellite Dataset")
all_sats = []
c = 0
for sat_data in data_all_sats:
    all_sats.append(ephem.readtle(sat_data["name"], sat_data["line1"], sat_data["line2"]))

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

inc_range = np.around(np.linspace(0,180,5), decimals=4)
raan_range = np.around(np.linspace(0,360,5), decimals=4)
# ecc_range = np.around(np.logspace(0,7, 15, base=10), decimals=0)
ecc_range = np.around(np.linspace(1,250000,5), decimals=0)
# print(ecc_range)
argp_range = np.around(np.linspace(0,360,5), decimals=4)
anom_range = np.around(np.linspace(0,360,5), decimals=4)
motion_range = np.around(np.linspace(11.25, 16,5), decimals=8)
# MAX MEAN MOTION = 16, LEO MIN MOTION = 11.25 
# print(motion_range)
special_sat_data = []
characters = {}
num_of_things = len(inc_range)*len(raan_range)*len(ecc_range)*len(argp_range)*len(anom_range)*len(motion_range)
c = 0
stack_num = 0
stack_pos = []




def get_abs(t, sat_real, sat_sim):
    timestep = datetime.fromtimestamp(t)
    sat_real.compute(timestep)
    sat_sim.compute(timestep)

    pos_real = np.array(compute_pos(sat_real.sublong, sat_real.sublat, sat_real.elevation))
    pos_sim = np.array(compute_pos(sat_sim.sublong, sat_sim.sublat, sat_sim.elevation))

    return np.linalg.norm(pos_real-pos_sim)-1000



data = []
c = 0
file_num = 0
for i, inc in enumerate(inc_range):
    print(100*i/len(inc_range), "%")
    for raan in raan_range:
        for ecc in ecc_range:
            for argp in argp_range:
                for anom in anom_range:
                    for motion in motion_range:
                        toccer.tic()
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
                        
                        sat_sim = ephem.readtle(fake_tle["name"], fake_tle["line1"], fake_tle["line2"])
                        
                        step_size = 1
                        t = START_TIME
                        adder = 0
                        
                        for sat_real in all_sats:
                            
                            try:
                                root = opt.root_scalar(get_abs, args=(sat_real, sat_sim), x0=START_TIME, x1=START_TIME+1, xtol=1, method="secant")
                                if (root).converged:
                                    adder += 1
                            except:
                                pass

                        data.append({
                            "inc":inc,
                            "raan": raan,
                            "ecc": ecc,
                            "argp": argp,
                            "anom": anom,
                            "motion": motion,
                            "conns": adder
                        })
                        

                        if c % 100 == 0 and c != 0:
                            save_json(save_location+"/big/"+str(file_num)+".json", data)
                            data = []
                            file_num += 1
                        c += 1

                        toccer.toc()

save_json(big_data_loc+"/"+str(c)+".json", data)

