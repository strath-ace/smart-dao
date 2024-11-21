import os
import datetime
from tqdm import tqdm
import itertools
import matplotlib.pyplot as plt

# Orbital Maths
from skyfield.api import load, utc
from sgp4.api import Satrec, WGS72
from skyfield.elementslib import osculating_elements_of

# GA
from pymoo.optimize import minimize
from pymoo.core.problem import ElementwiseProblem, Problem
from pymoo.core.mixed import MixedVariableGA
from pymoo.core.variable import Real
from pymoo.optimize import minimize
from pymoo.core.evaluator import Evaluator
from pymoo.core.population import Population
from pymoo.algorithms.moo.nsga2 import NSGA2

from common import *
from ga_fitness import fitness

open_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(open_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)



ts = load.timescale()

start_date = datetime.datetime(2024,9,11, tzinfo=utc)
end_date = start_date + relativedelta(days=1)
time_range = date_range(start_date, end_date, 30, 'seconds')
time = ts.from_datetimes(time_range)
epoch = (start_date - datetime.datetime(1949,12,31,0,0, tzinfo=utc))




satellites = get_icsmd_satellites(open_location+"/active.tle", "icsmd_sats.txt")

# REMOVE
# satellites = satellites[:len(satellites)//3]










class MyProblem(Problem):
    def __init__(self, possible, real_sat_grid, time, **kwargs):
        super().__init__(
            n_var=6, 
            n_obj=2, 
            xl=np.array([-180, 0, -90, -180, -180, 4000]), 
            xu=np.array([180, 0.14, 90, 180, 180, 6500]),
            **kwargs
        )
        self.possible = possible
        self.real_sat_grid = real_sat_grid
        self.time = time

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = []
        f2 = []
        # print(x)
        for val in tqdm(x, desc="Consensus on population"):
            argp_i = val[0]
            ecc_i = val[1]
            inc_i = val[2]
            raan_i = val[3]
            anom_i = val[4]
            mot_i = val[5]
            # print(val)
            satellite2 = Satrec()
            satellite2.sgp4init(
                WGS72,                      # gravity model
                'i',                        # 'a' = old AFSPC mode, 'i' = improved mode
                25544,                      # satnum: Satellite number
                epoch.days,                 # epoch: days since 1949 December 31 00:00 UT
                3.8792e-05,                 # bstar: drag coefficient (1/earth radii)
                0.0,                        # ndot: ballistic coefficient (radians/minute^2)
                0.0,                        # nddot: mean motion 2nd derivative (radians/minute^3)
                ecc_i,                      # ecco: eccentricity
                np.deg2rad(argp_i),         # argpo: argument of perigee (radians)
                np.deg2rad(inc_i),          # inclo: inclination (radians)
                np.deg2rad(anom_i),         # mo: mean anomaly (radians)
                np.deg2rad(mot_i)/(24*60),  # no_kozai: mean motion (radians/minute)
                np.deg2rad(raan_i),         # nodeo: R.A. of ascending node (radians)
            )
            sim_sat = EarthSatellite.from_satrec(satellite2, ts)
            completed, time = fitness(sim_sat, satellites, self.possible.copy(), self.real_sat_grid, self.time)
            f1.append(-completed)
            f2.append(time)
        # print(f1,f2)
        out["F"] = np.column_stack([f1, f2])




########## Get all valid combinations

valid_combs = []
valid_combs_time = []
for i, x in enumerate(tqdm(satellites, desc="Building possible real satellite combinations")):
    for j, y in enumerate(satellites):
        if j > i:
            barycentric = (x.at(time) - y.at(time)).distance().km
            ans = np.where(barycentric <= 500)[0]
            if len(ans) > 0:
                valid_combs.append([i, j])
                valid_combs_time.append(ans)

valid_combs = np.array(valid_combs)       

def checker(temp):
    for i, x in enumerate(temp):
        for j, y in enumerate(temp):
            if j > i:
                if not y in valid_combs[valid_combs[:,0] == x, 1]:
                    return False
    return True

possible = filter(checker, itertools.combinations(np.arange(0,np.amax(valid_combs)), 3))
possible = np.array(list(possible))



######### Create real sat grid

big_comb = np.array(satellites)

real_sat_grid = np.zeros((len(big_comb), len(big_comb), len(time)))
real_sat_grid[real_sat_grid == 0] = np.nan

for i in tqdm(range(len(big_comb)), desc="Generate real satellite's interactions"):
    for j in range(len(big_comb)):
        if i != j:
            x = np.where((big_comb[i].at(time) - big_comb[j].at(time)).distance().km <= 500)[0]
            real_sat_grid[i,j,:len(x)] = x
            real_sat_grid[j,i,:len(x)] = x




problem = MyProblem(possible, real_sat_grid, time)





# Generate initial guess from a different satellite
barycentric = satellites[1].at(ts.from_datetime(start_date))
orb = osculating_elements_of(barycentric)
X = {
    'argp_i': orb.argument_of_periapsis.degrees,
    'ecc_i': orb.eccentricity, 
    'inc_i': orb.inclination.degrees, 
    'raan_i': orb.longitude_of_ascending_node.degrees, 
    'anom_i': orb.mean_anomaly.degrees, 
    'mot_i': orb.mean_motion_per_day.degrees
}

X = [
    orb.argument_of_periapsis.degrees,
    orb.eccentricity, 
    orb.inclination.degrees, 
    orb.longitude_of_ascending_node.degrees, 
    orb.mean_anomaly.degrees, 
    orb.mean_motion_per_day.degrees
]

pop = Population.new("X", [X])
Evaluator().eval(problem, pop)




pop_size = 50
num_generations = 50


# algorithm = MixedVariableGA(
#     pop_size=int(pop_size), sampling=pop)


algorithm = NSGA2(pop_size=int(pop_size))
                    # sampling=pop,
                    # eliminate_duplicates=True)

res = minimize(problem,
               algorithm,
               ("n_gen", int(num_generations)),
               seed=1,
               verbose=True,
               save_history=True)

print()
print("------ RESULTS ------")
print("Maximum consensus:", res.F, "%")
print("Orbital Elements:",res.X)

print()

out_data = []
for i in range(len(res.history)):
    out_data.append({
        "gen": i,
        # "x": res.history[i].pop.get("X").tolist(),
        "non-dominated-solutions": res.history[i].pop.get("F").tolist()
    })

save_json("data-ga/"+str(round(datetime.datetime.now().timestamp()))+".json", out_data)