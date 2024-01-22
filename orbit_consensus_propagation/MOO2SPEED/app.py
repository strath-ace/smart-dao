# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

from pymoo.optimize import minimize
from pymoo.problems.functional import FunctionalProblem
from pymoo.core.problem import Problem
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
from array import array


########################## PARAMATERS #########################

##### PROBLEM PARAMS #####
# Number of satellites to include
n_vars = 82
# Max number of satellites in subset (Must be less than n_vars)
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

consensus_core = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "CONSENSUSSPEED")
if not os.path.exists(consensus_core):
    raise Exception("Consensus Core does not exist (../consensus/.)")

MAX_TIME = load_json(save_location+"/dataset.json")["max_time"]

######################### BUILD GO FUNCTIONS FOR CONSENSUS #########################

os.system("go build -buildmode=c-shared -o "+consensus_core+"/consensus.so "+consensus_core+"/.")

library = ctypes.CDLL(consensus_core+"/consensus.so") # On linux put .dll rather than .so

conn4 = library.consensus_time4
conn4.argtypes = [
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_longlong,
    ]

completer_per = library.consensus_completeness_per
completer_per.argtypes = [
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_longlong,
    ]

counter_array = []
temp = []
for i in range(n_vars):
    temp.append(i)
counter_array = np.asanyarray(temp, dtype=int)

starter = []
for i in range(n_vars):
    starter.append(0)
# print(counter_array)
######################### CONSENSUS FUNCTION CALLS #########################

def convert_to_json(x):
    genetics = []
    for y in x:
        genetics.append(counter_array[y.astype(bool)].tolist())
    return genetics

def json_og(x):
    genetics = []
    for y in x:
        genetics.append(counter_array[y.astype(bool)].tolist())
    document = {
        "ids": genetics
    }
    return document

def fit4(x):
    out = array('d', starter)
    out_ptr = (ctypes.c_double * len(out)).from_buffer(out)

    conn4(json.dumps(json_og(x)).encode('utf-8'), out_ptr, len(out))
    stuff = np.array(list(out))
    indx = stuff <= 4
    stuff = (stuff-START_TIME)/MAX_TIME
    stuff[indx] = 1
    return stuff


def completeness_per(x):
    out = array('d', starter)
    out_ptr = (ctypes.c_double * len(out)).from_buffer(out)

    completer_per(json.dumps(json_og(x)).encode('utf-8'), out_ptr, len(out))
    return np.array(list(out))/10000

######################### OPTIMISATION STRATEGY #########################




class MyProblem(Problem):
    def __init__(self):
        super().__init__(n_var=n_vars, n_obj=2, n_ieq_constr=2)
        
    def _evaluate(self, x, out):
        f1 = fit4(x)
        f2 = -(np.sum(x, axis=1))
        c1 = 4 - np.sum(x, axis=1)
        c2 = 1 - completeness_per(x)
        out["F"] = np.column_stack([f1, f2])
        out["G"] = np.column_stack([c1, c2])

problem = MyProblem()

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