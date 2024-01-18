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

######### INPUT PARAMS

TIMESTEP = 60
NUM_ITERATIONS = 1440

SAVE_DIR = "data_icsmd"

STACK_SIZE = 100

DIS = 1000*1000

######### BUILD C/GO code

try:
    os.system("go build -buildmode=c-shared -o combinatorics.so combinatorics.go")
except:
    raise Exception("Did not compile") 

library = ctypes.cdll.LoadLibrary('./combinatorics.so')

combinations = library.combinations
combinations.argtypes = [ctypes.c_char_p]
combinations.restype = ctypes.c_void_p

######### LOAD DATASETS

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_DIR)
if not os.path.exists(save_location):
    os.makedirs(save_location)
real_data = os.path.join(save_location, "real.npy")
if not os.path.exists(real_data):
    real_exist = False
else:
    real_exist = True
sim_data = os.path.join(save_location, "params")
if not os.path.exists(sim_data):
    os.makedirs(sim_data)
sim_results = os.path.join(save_location, "results")
if not os.path.exists(sim_results):
    os.makedirs(sim_results)

data_all_sats = load_json(save_location+"/sorted_sats.json")

START_TIME = load_json(save_location+"/dataset.json")["timestamp"]

iterations = np.linspace(START_TIME, START_TIME+(NUM_ITERATIONS*TIMESTEP), NUM_ITERATIONS)

######### GET POSITIONS OF SATELLITES IN DATASET
t = TicToc()


if not real_exist:
    print("Generating Real Satellite Dataset")
    t.tic()
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
    np.save(real_data, all_real_pos)
    print("Real Satellite Dataset Generated")
    t.toc()




def computer(stack_sim_pos, i, all_real_pos):
    t.tic()
    print("Saving")
    document = {
        "counter": [[[i]]],
        "real": all_real_pos.tolist(),
        "sim": stack_sim_pos.tolist()
    }
    combinations(json.dumps(document).encode('utf-8'))
    t.toc()


t.tic()
all_real_pos = np.load(real_data)
print("Real Data Load")
t.toc()


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
num_of_things = len(inc_range)*len(raan_range)*len(ecc_range)*len(argp_range)*len(anom_range)*len(motion_range)
c = 0
stack_num = 0
stack_pos = []

try:
    starting_stack = load_json(save_location+"/last_calc.json")["last_calc"]
    kick_off = False
except:
    starting_stack = 0
    kick_off = True



for i, inc in enumerate(inc_range):
    print(100*i/len(inc_range), "%")
    for raan in raan_range:
        for ecc in ecc_range:
            for argp in argp_range:
                for anom in anom_range:
                    for motion in motion_range:#
                        if c >= STACK_SIZE and not kick_off:
                            stack_num += 1
                            c = 0
                            continue
                        elif stack_num <= starting_stack and not kick_off:
                            c += 1
                            continue
                        else:
                            kick_off = True
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
                            characters.update({c: {"inc":inc, 
                                                "raan":raan,
                                                "ecc":ecc,
                                                "argp":argp,
                                                "anom":anom,
                                                "motion":motion
                                                }})
                            if c >= STACK_SIZE and kick_off:
                                # print("SAVING")
                                # csv_output(sim_data+"/"+str(c)+".csv", pos)
                                # asyncio.run(computer(np.array(stack_pos), c, np.array(all_real_pos)))
                                computer(np.array(stack_pos), stack_num, np.array(all_real_pos))
                                # print("SAVE1")
                                save_json(save_location+"/params/"+str(stack_num)+".json", characters)
                                save_json(save_location+"/last_calc.json", {"last_calc": stack_num-1})
                                print("Stack",stack_num,"done out of",num_of_things/STACK_SIZE)  
                                stack_num += 1
                                c = 0
                                stack_pos = []
                                characters = {}
                            else:
                                c += 1                            
                        except:
                            raise Exception(t2, "didnt work") 

computer(stack_pos, stack_num)
save_json(save_location+"/params/"+str(stack_num)+".json", characters)










