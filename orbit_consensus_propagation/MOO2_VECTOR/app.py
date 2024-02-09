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
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.core.problem import Problem
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.operators.sampling.rnd import IntegerRandomSampling
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
from pytictoc import TicToc


########################## PARAMATERS #########################

##### OPTIMISER PARAMS #####
# Size of the population for each generation
population_size = 50
# Number of generations of population to optimise across
num_gens = 1000
# Probability of Crossover (0 - 1)
cross_prob = 0.1
# Probability of random mutation (0 - 1)
mut_prob = 0.1

NUM_TIMES = 200

NO_DISPLAY = True

##### PROBLEM PARAMS #####
# Number of satellites to include
n_vars = 82
# Max number of satellites in subset (Must be less than n_vars)
max_sat = 82



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
if config["START_TIME"] != round(START_TIME):
    config["START_TIME"] = round(START_TIME)

    with open(this_location+"/config.yml", "w") as f:
        yaml.dump(config, f)


opt_location = os.path.join(save_location, "moo2")
if not os.path.exists(opt_location):
    os.makedirs(opt_location)
opt_data = os.path.join(opt_location, "data")
if not os.path.exists(opt_data):
    os.makedirs(opt_data)

consensus_core = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "CONSENSUS_BULK")
if not os.path.exists(consensus_core):
    raise Exception("Consensus Core does not exist (../CONSENSUS_BULK/.)")

MAX_TIME = load_json(save_location+"/dataset.json")["max_time"]

if NO_DISPLAY:
    all_display = False
else:
    all_display = True

######################### BUILD GO FUNCTIONS FOR CONSENSUS #########################

os.system("go build -buildmode=c-shared -o "+consensus_core+"/consensus.so "+consensus_core+"/.")

library = ctypes.CDLL(consensus_core+"/consensus.so") # On windows put .dll rather than .so

combined_fit= library.consensus_combined_fit
combined_fit.argtypes = [
    ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_longlong,
    ]

counter_array = []
temp = []
for i in range(n_vars):
    temp.append(i)
counter_array = np.asanyarray(temp, dtype=int)

######################### CONSENSUS FUNCTION CALLS #########################

def json_og(x):
    genetics = []
    for y in x:
        genetics.append(counter_array[y.astype(bool)].tolist())
    document = {
        "ids": genetics
    }
    return document

# def json_2(x):
#     genetics = []
#     for y in x:
#         genetics.append((y[y>0]-1).tolist())
#     document = {
#         "ids": genetics
#     }
#     return document

def combined_stuff(x):
    out_fit = array('d', np.zeros(population_size))
    out_fit_ptr = (ctypes.c_double * len(out_fit)).from_buffer(out_fit)
    out_comp = array('d', np.zeros(population_size))
    out_comp_ptr = (ctypes.c_double * len(out_comp)).from_buffer(out_comp)
    combined_fit(json.dumps(json_og(x)).encode('utf-8'), out_fit_ptr, out_comp_ptr, len(out_fit))
    # combined_fit(json.dumps(json_2(x)).encode('utf-8'), out_fit_ptr, out_comp_ptr, len(out_fit))

    stuff = np.array(list(out_fit))
    indx = stuff <= 4
    stuff = (stuff-START_TIME)/MAX_TIME
    stuff[indx] = 1

    stuff2 = np.array(list(out_comp))

    return stuff, stuff2

######################### OPTIMISATION STRATEGY #########################

for STEPPER in range(NUM_TIMES):
    # try:
    class MyProblem(Problem):
        def __init__(self):
            # super().__init__(n_var=n_vars, n_obj=2, n_ieq_constr=2, xl=0, xu=82, vtype=int)
            super().__init__(n_var=n_vars, n_obj=2, n_ieq_constr=2)
            
        def _evaluate(self, x, out):
            fitness, completeness = combined_stuff(x)
            # summer = np.sum(x > 0, axis=1)
            summer = np.sum(x, axis=1)
            f1 = fitness
            f2 = -summer
            c1 = 4 - summer
            c2 = 1 - completeness
            out["F"] = np.column_stack([f1, f2])
            out["G"] = np.column_stack([c1, c2])

    problem = MyProblem()

    algorithm = NSGA2(pop_size=population_size,
                    sampling=BinaryRandomSampling(),
                    crossover=TwoPointCrossover(prob=cross_prob),
                    mutation=BitflipMutation(prob=mut_prob),
                    eliminate_duplicates=True,
                    save_history=all_display)

    

    # algorithm = NSGA2(pop_size=population_size,
    #                 sampling=IntegerRandomSampling(),
    #                 crossover=SBX(prob=cross_prob, eta=3.0, vtype=float, repair=RoundingRepair()),
    #                 mutation=PM(prob=mut_prob, eta=3.0, vtype=float, repair=RoundingRepair()),
    #                 eliminate_duplicates=True,
    #                 save_history=all_display)
    

    from pymoo.termination.ftol import MultiObjectiveSpaceTermination
    from pymoo.termination.robust import RobustTermination


    termination = RobustTermination(MultiObjectiveSpaceTermination(tol=0.0001, n_skip=50), period=20)

    # 0.0001
    # 50

    ticer2 = TicToc()
    ticer2.tic()
    res = minimize(problem,
                algorithm,
                termination,
                verbose=True,
                save_history=all_display)
    print("FINAL TIME:")
    ticer2.toc()
    ######################### SAVE OUTPUT #########################

    if NO_DISPLAY:
        print("#####################")
        print("RESULTS:")
        for x in res.opt:
            print(x.get("F"), "from", counter_array[x.get("X")])
        np.savez(opt_data+"/"+str(round(time.time()))[3:], X=res.opt.get("X"), F=res.opt.get("F"))   
    else:
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
    # except:
    #     pass