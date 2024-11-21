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

from common import *
from ga_fitness import *

open_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(open_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)


num_start_days = 10
pop_size = 50
num_generations = 50
num_sim_sats = 1
number_of_replicas = 4
run_mode = "completed" # "time"



class MyProblem(Problem):
    def __init__(self, num_sim_sats, possible, real_sat_grid, time, mode, b, **kwargs):
        vars = {}
        for i in range(num_sim_sats):
            vars.update({"argp_i_"+str(i): Real(bounds=(-180, 180))})
            vars.update({"ecc_i_"+str(i): Real(bounds=(0, 0.14))})
            vars.update({"inc_i_"+str(i): Real(bounds=(-90, 90))})
            vars.update({"raan_i_"+str(i): Real(bounds=(-180, 180))})
            vars.update({"anom_i_"+str(i): Real(bounds=(-180, 180))})
            vars.update({"mot_i_"+str(i): Real(bounds=(4000, 6500))})
        super().__init__(vars=vars, n_obj=1, **kwargs)
        self.possible = possible
        self.real_sat_grid = real_sat_grid
        self.time = time
        self.num_sim_sats = num_sim_sats
        self.mode = mode
        self.b = b

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = []
        for val in tqdm(x, desc="Consensus on population"):
            sim_sats = []
            for i in range(self.num_sim_sats):
                argp_i = val["argp_i_"+str(i)]
                ecc_i = val["ecc_i_"+str(i)]
                inc_i = val["inc_i_"+str(i)]
                raan_i = val["raan_i_"+str(i)]
                anom_i = val["anom_i_"+str(i)]
                mot_i = val["mot_i_"+str(i)]
                sim_sat = Satrec()
                sim_sat.sgp4init(
                    WGS72,                      # gravity model
                    'i',                        # 'a' = old AFSPC mode, 'i' = improved mode
                    25544+i,                      # satnum: Satellite number
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
                sim_sats.append(EarthSatellite.from_satrec(sim_sat, ts))
            completed, time = fitness_multi_sat(sim_sats, satellites, self.possible.copy(), self.real_sat_grid, self.time, self.b)
            if self.mode == "completed":
                f1.append(-completed)
            elif self.mode == "time":
                f1.append(time)
            else:
                raise Exception("Mode not correctly defined")
        out["F"] = f1



for start_day_added in range(num_start_days):

    ts = load.timescale()

    start_date = datetime.datetime(2024,9,11+start_day_added, tzinfo=utc)
    end_date = start_date + relativedelta(days=1)
    time_range = date_range(start_date, end_date, 30, 'seconds')
    time = ts.from_datetimes(time_range)
    epoch = (start_date - datetime.datetime(1949,12,31,0,0, tzinfo=utc))


    satellites = get_icsmd_satellites(open_location+"/active.tle", "icsmd_sats.txt")

    # REMOVE
    # satellites = satellites[:len(satellites)//4]



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

    possible = filter(checker, itertools.combinations(np.arange(0,np.amax(valid_combs)), number_of_replicas-num_sim_sats))
    possible = np.array(list(possible))



    ######### Create real sat grid

    big_comb = np.array(satellites)

    real_sat_grid = np.zeros((len(big_comb), len(big_comb), len(time)))
    real_sat_grid[real_sat_grid == 0] = np.nan
    b = 0
    for i in tqdm(range(len(big_comb)), desc="Generate real satellite's interactions"):
        for j in range(len(big_comb)):
            if i != j:
                x = np.where((big_comb[i].at(time) - big_comb[j].at(time)).distance().km <= 500)[0]
                if len(x) > b:
                    b = len(x)
                real_sat_grid[i,j,:len(x)] = x
                real_sat_grid[j,i,:len(x)] = x




    problem = MyProblem(num_sim_sats, possible, real_sat_grid, time, run_mode, b)





    # Generate initial guess from a different satellite
    # barycentric = satellites[1].at(ts.from_datetime(start_date))
    # orb = osculating_elements_of(barycentric)

    X = {}
    for i in range(num_sim_sats):
        barycentric = satellites[0].at(ts.from_datetime(start_date))
        orb = osculating_elements_of(barycentric)   
        X.update({"argp_i_"+str(i): orb.argument_of_periapsis.degrees})
        X.update({"ecc_i_"+str(i): orb.eccentricity})
        if i == 1:
            X.update({"inc_i_"+str(i): -orb.inclination.degrees})
        else:
            X.update({"inc_i_"+str(i): orb.inclination.degrees})
        X.update({"raan_i_"+str(i): orb.longitude_of_ascending_node.degrees})
        X.update({"anom_i_"+str(i): orb.mean_anomaly.degrees})
        X.update({"mot_i_"+str(i): orb.mean_motion_per_day.degrees})

    print(X)
    pop = Population.new("X", [X])
    Evaluator().eval(problem, pop)







    algorithm = MixedVariableGA(
        pop_size=int(pop_size), sampling=pop)

    res = minimize(problem,
                algorithm,
                ("n_gen", int(num_generations)),
                seed=1,
                verbose=True,
                save_history=True)

    print()
    print("------ RESULTS ------")
    print("Maximum consensus:", round(-res.F[0]*100,2), "%")
    print("Orbital Elements:",res.X)

    print()

    out_data = []
    for i in range(len(res.history)):
        out_data.append({
            "gen": i,
            "x": res.history[i].pop.get("X").tolist(),
            "f": res.history[i].pop.get("F")[:,0].tolist()
        })

    # save_json("data-ga/"+str(round(datetime.datetime.now().timestamp()))+".json", out_data)
    save_json("data-ga/"+str(start_day_added)+"_"+run_mode+".json", out_data)