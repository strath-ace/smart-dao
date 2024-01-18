import ctypes
import os
import json
import ephem
import numpy as np
import math
from datetime import datetime
from generic import *
from pytictoc import TicToc
from geneticalgorithm import geneticalgorithm as ga

######### INPUT PARAMS

START_TIME = 1701448313
TIMESTEP = 60
NUM_ITERATIONS = 100*60

GA_num_iterations = 1
GA_pop_size = 200   # My PC doesnt max out at this size?
GA_mutat = 0.25
GA_dim = 4

REBUILD = False

######### LOAD LIBRARIES

os.system("go build -buildmode=c-shared -o library.so library.go")

library = ctypes.cdll.LoadLibrary('./library.so')

consensus_time = library.consensus_time
consensus_time.argtypes = [ctypes.c_char_p]
consensus_time.restype = ctypes.c_void_p

######### LOAD DATASETS

iterations = np.linspace(START_TIME, START_TIME+(NUM_ITERATIONS*TIMESTEP), NUM_ITERATIONS)


save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)
big_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "big")
if not os.path.exists(big_data):
    os.makedirs(big_data)

data_all_sats = load_json(save_location+"/sorted_sats.json")

######### GET POSITIONS OF SATELLITES IN DATASET

if REBUILD:
    all_sats = []
    for sat_data in data_all_sats:
        all_sats.append(ephem.readtle(sat_data["name"], sat_data["line1"], sat_data["line2"]))

    for order, sat in enumerate(all_sats):
        pos = []
        for i in iterations:
            timestep = datetime.fromtimestamp(i)
            sat.compute(timestep)
            pos.append(compute_pos(sat.sublong, sat.sublat, sat.elevation))

        # SAVE POS in FILE
        csv_output(big_data+"/"+str(order)+".csv", pos)

    print("Dataset generated")

######### DEFINED FITNESS ALGORITHM

def fitness(genetics):
    genetics = genetics.astype(np.int64).tolist()
    # print(genetics)
    document = {
        "ids": genetics
    }
    out = consensus_time(json.dumps(document).encode('utf-8'))
    if out == -1:
        return "FAILURE"
    else:
        return out*TIMESTEP/(60*60)
    
######### START GENETIC ALGORITHM

print("Genetic Algorithm Starting")

# There are 2^num_sats total combinations
var_bound = []
for i in range(GA_dim):
    var_bound.append([0,81])
var_bound = np.asarray(var_bound, dtype=(int))
# 0.01
# 0.5
file_save="data/plotted.png"
algorithm_param = {'max_num_iteration': GA_num_iterations,\
                   'population_size':GA_pop_size,\
                   'mutation_probability':GA_mutat,\
                   'elit_ratio': 0,\
                   'crossover_probability': 0.5,\
                    'parents_portion': 0.3,\
                   'crossover_type':'uniform',\
                   'max_iteration_without_improv':None}
model=ga(save_file=file_save, function=fitness,dimension=GA_dim,variable_type='int',variable_boundaries=var_bound,algorithm_parameters=algorithm_param)

t=TicToc(); t.tic()
model.run()
t.toc()

print("-----------")
print("For GA with", GA_num_iterations, "iterations,", GA_pop_size, "population size and", GA_mutat, "mutation probability")

convergence=model.report
solution=model.output_dict
print(convergence)
print(solution)
print(model)
