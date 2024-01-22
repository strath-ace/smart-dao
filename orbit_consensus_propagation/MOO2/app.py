# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

from pymoo.optimize import minimize
from pymoo.problems.functional import FunctionalProblem
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.optimize import minimize

import ctypes as ctypes
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import time
import yaml
from commons import *

########################## PARAMATERS #########################

##### PROBLEM PARAMS #####
# Number of satellites to include
n_var = 82
# Max number of satellites in subset (Must be less than n_var)
max_sat = 82

##### OPTIMISER PARAMS #####
# Size of the population for each generation
population_size = 400
# Number of generations of population to optimise across
num_gens = 400
# Probability of Crossover (0 - 1)
cross_prob = 0.1
# Probability of random mutation (0 - 1)
mut_prob = 0.1

######################### BUILD/FIND DIRECTORIES FOR DATA #########################

this_location = os.path.join(os.path.dirname(os.path.abspath(__file__)))

# Open Yaml
with open(this_location+"/config.yml") as f:
     config = yaml.safe_load(f)

SAVE_DIR = config["BIG_DATA"]

# Get save location
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("Data File does not exist")

# Get start time from save_location
START_TIME = load_json(save_location+"/dataset.json")["timestamp"]

# Update config file with start time
config["START_TIME"] = round(START_TIME)

# Comment these lines to run in parallel
with open(this_location+"/config.yml", "w") as f:
    yaml.dump(config, f)


opt_location = os.path.join(save_location, "moo2")
if not os.path.exists(opt_location):
    os.makedirs(opt_location)
opt_data = os.path.join(opt_location, "data")
if not os.path.exists(opt_data):
    os.makedirs(opt_data)

consensus_core = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "CONSENSUS")
if not os.path.exists(consensus_core):
    raise Exception("Consensus Core does not exist (../consensus/.)")

MAX_TIME = load_json(save_location+"/dataset.json")["max_time"]

######################### BUILD GO FUNCTIONS FOR CONSENSUS #########################

os.system("go build -buildmode=c-shared -o "+consensus_core+"/consensus.so "+consensus_core+"/.")

library = ctypes.cdll.LoadLibrary(consensus_core+"/consensus.so")

conn1 = library.consensus_time1
conn1.argtypes = [ctypes.c_char_p]
conn1.restype = ctypes.c_void_p
conn2 = library.consensus_time2
conn2.argtypes = [ctypes.c_char_p]
conn2.restype = ctypes.c_void_p
conn3 = library.consensus_time3
conn3.argtypes = [ctypes.c_char_p]
conn3.restype = ctypes.c_void_p
conn4 = library.consensus_time4
conn4.argtypes = [ctypes.c_char_p]
conn4.restype = ctypes.c_void_p

completer_abs = library.consensus_completeness_abs
completer_abs.argtypes = [ctypes.c_char_p]
completer_abs.restype = ctypes.c_void_p

completer_per = library.consensus_completeness_per
completer_per.argtypes = [ctypes.c_char_p]
completer_per.restype = ctypes.c_void_p

counter_array = []
for i in range(n_var):
    counter_array.append(i)
counter_array = np.array(counter_array)

######################### CONSENSUS FUNCTION CALLS #########################

def convert_to_json(x):
    genetics = counter_array[x.astype(bool)]
    genetics = genetics.astype(np.int64).tolist()
    # print(genetics)
    document = {
        "ids": genetics
    }
    return document

def fit1(x):
    out = conn1(json.dumps(convert_to_json(x)).encode('utf-8'))
    if out in [1,2,3,4]:
        return 1
    return (out-START_TIME)/MAX_TIME

def fit2(x):
    out = conn2(json.dumps(convert_to_json(x)).encode('utf-8'))
    if out in [1,2,3,4]:
        return 1
    return (out-START_TIME)/MAX_TIME

def fit3(x):
    out = conn3(json.dumps(convert_to_json(x)).encode('utf-8'))
    if out in [1,2,3,4]:
        return 1
    return (out-START_TIME)/MAX_TIME

def fit4(x):
    out = conn4(json.dumps(convert_to_json(x)).encode('utf-8'))
    if out in [1,2,3,4]:
        return 1
    return (out-START_TIME)/MAX_TIME

def completeness_abs(x):
    out = completer_abs(json.dumps(convert_to_json(x)).encode('utf-8'))
    return out

def completeness_per(x):
    out = completer_per(json.dumps(convert_to_json(x)).encode('utf-8'))
    return out/10000

######################### OPTIMISATION STRATEGY #########################

objs = [
    # lambda x: -completeness_per(x),
    lambda x: fit4(x),
    lambda x: -(np.sum(x))
]

constr_ieq = [
    lambda x: 4 - np.sum(x),    # Make sure num satellites is >=  4
    lambda x: np.sum(x) - max_sat,    # Only calculate for num satellites up to 40 in subset
    lambda x: 1 - completeness_per(x)
]
# num_sats >= 4
# 0 >= 4 - num_sats

problem = FunctionalProblem(n_var,
                            objs,
                            constr_ieq=constr_ieq
                            )


algorithm = NSGA2(pop_size=population_size,
                  sampling=BinaryRandomSampling(),
                  crossover=TwoPointCrossover(prob=cross_prob),
                  mutation=BitflipMutation(prob=mut_prob),
                  eliminate_duplicates=True,
                  save_history=True)

res = minimize(problem,
               algorithm,
               ('n_gen', num_gens),
               verbose=True,
               save_history=True)

######################### SAVE OUTPUT #########################

output_X = []
output_F = []
for i in range(len(res.history)):
    output_X.append(res.history[i].pop.get("X").tolist())
    output_F.append(res.history[i].pop.get("F").tolist())

np.savez(opt_data+"/run_"+str(round(time.time()))[3:]+"_x", *output_X)    
np.savez(opt_data+"/run_"+str(round(time.time()))[3:]+"_f", *output_F)

try:
    print("Result:", res.F[res.F[:,0] != MAX_TIME])
except:
    print("No results")