import os
import datetime
from tqdm import tqdm
from functools import reduce

# Orbital Maths
from skyfield.api import load, utc

# GA
from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from pymoo.core.mixed import MixedVariableGA
from pymoo.core.variable import Real
from pymoo.optimize import minimize

# Golang call
import ctypes
from array import array

# My other functions
from common import *
from ga_func import *

################## Parameters ##################

pop_size = 200
num_generations = 50
num_start_days = 10
max_consensus_time = 0.1  # Days

num_participants = 4

################## Get file paths for loading and saving data ##################

open_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(open_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data-ga")
if not os.path.exists(save_location):
    os.makedirs(save_location)

################## Build golang fitness function ##################

os.system("go build -buildmode=c-shared -o ./go_fit.so .")

################## Load real satellites from subset ##################

satellites = get_satellites(open_location+"/active.tle", refine_by_name="icsmd_sats.txt")

################## Define GA method ##################

class MyProblem(Problem):
    def __init__(self, possible, real_sat_grid, time, num_participants=4, **kwargs):
        vars = {
            "argp_i": Real(bounds=(-180, 180)),
            "ecc_i": Real(bounds=(0, 0.14)),
            "inc_i": Real(bounds=(-90, 90)),
            "raan_i": Real(bounds=(-180, 180)),
            "anom_i": Real(bounds=(-180, 180)),
            "mot_i": Real(bounds=(4000, 6500)),
        }
        super().__init__(vars=vars, n_obj=1, **kwargs)
        
        self.regen = len(possible)

        combs_all = []
        for pos in possible:
            combs_arr = array('d', (pos).flatten().tolist())
            combs_raw = (ctypes.c_double * len(combs_arr)).from_buffer(combs_arr)
            combs_all.append(combs_raw)

        self.possible = combs_all
        if len(possible) > 0:
            self.num_participants = num_participants
        else:
            self.num_participants = 1
        real_sat_grid_flat = []
        for i, real_sats in enumerate(real_sat_grid):
            real_sat_grid_flat.append(np.array(flatten_plus_one(real_sats, time[i]), dtype=float))
        self.real_sat_grid_flat = real_sat_grid_flat
        self.depth = np.shape(real_sat_grid)[3]
        self.time = time
        

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = []
        for orbit_elements in tqdm(x, desc="Consensus on population"):
            gen_date = datetime.datetime(2024,9,11, tzinfo=utc)
            epoch = (gen_date - datetime.datetime(1949,12,31,0,0, tzinfo=utc))
            sim_sat = make_satellite(orbit_elements, epoch, ts)
            values = []
            for i in range(self.regen):
                if len(self.possible[i]) > 0:
                    completed = fitness(sim_sat, satellites, self.possible[i], self.real_sat_grid_flat[i].copy(), self.depth, self.time[i].tolist(), self.num_participants)
                    completed = len(completed) - [16,15,9,14,19,18,15,4,12,13][i]
                else:
                    completed = 0
                values.append(-completed)
            f1.append(np.mean(values))
        out["F"] = f1




# For each start day
possible = []
real_sat_grid_all = []
time_all = []
for start_day_added in range(num_start_days):

    ################## Generate time frame information ##################

    ts = load.timescale()
    start_date = datetime.datetime(2024,9,11+start_day_added, tzinfo=utc)
    end_date = start_date + relativedelta(days=max_consensus_time)
    time_range = date_range(start_date, end_date, 30, 'seconds')
    time_all.append(time_range)
    time = ts.from_datetimes(time_range)
    
    
    ################## Pre-Generate real satellite interaction grid ##################

    
    big_comb = np.array(satellites)
    real_sat_grid = np.zeros((len(big_comb), len(big_comb), len(time)))
    real_sat_grid[real_sat_grid == 0] = -1
    gg = []
    for i in tqdm(range(len(big_comb)), desc="Generate real sats day "+str(start_day_added)):
        for j in range(len(big_comb)):
            if i != j:
                x = np.where((big_comb[i].at(time) - big_comb[j].at(time)).distance().km <= 500)[0]
                real_sat_grid[i,j,:len(x)] = x
                real_sat_grid[j,i,:len(x)] = x
                if len(x) > 0:# and j > i:
                    gg.append([i+1,j+1])

    real_sat_grid_all.append(real_sat_grid)

    for i in range(len(satellites)):
        gg.append([0,i+1])
    gg = np.array(gg)

    ################## Combination builder ##################

    # Creates possible combinations from satellites that can see each other
    
    pos_last = gg.copy()
    while len(pos_last) > 0 and np.shape(pos_last)[1] < num_participants:
        pos = pos_last.copy()
        pos_last = []
        for item in pos:
            x_vals = []
            for itemx in item:
                x_vals.append(np.unique(np.append(gg[gg[:,0] == itemx, 1], gg[gg[:,1] == itemx, 0])))
            for x in reduce(np.intersect1d, x_vals):
                pos_last.append([*item, x])

    possible.append(np.array(pos_last))
    
    # print("Possible satellite consensus combinations:", np.shape(possible))

################## Start GA ##################

time_all = np.array(time_all)
real_sat_grid_all = np.array(real_sat_grid_all)
# possible = np.array(possible)

problem = MyProblem(possible, real_sat_grid_all, time_all)


algorithm = MixedVariableGA(
    pop_size=int(pop_size))#, sampling=pop)

res = minimize(problem,
            algorithm,
            ("n_gen", int(num_generations)),
            seed=1,
            verbose=True,
            save_history=True)

print("Finished")
print()

################## Save GA history ##################

out_data = []
for i in range(len(res.history)):
    out_data.append({
        "gen": i,
        "x": res.history[i].pop.get("X").tolist(),
        "f": res.history[i].pop.get("F")[:,0].tolist()
    })

file_name = save_location+"/"
file_name += "participants_"+str(num_participants)+"_"
file_name += "startday_special2_"
file_name += "conntime_{:02d}".format(int(max_consensus_time*10))
file_name += ".json"
save_json(file_name, out_data)