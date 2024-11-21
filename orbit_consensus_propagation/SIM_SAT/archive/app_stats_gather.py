import numpy as np
import os
import ctypes
from array import array
from pytictoc import TicToc

import datetime
from tqdm import tqdm
import itertools
import matplotlib.pyplot as plt

# Orbital Maths
from skyfield.api import load, utc
from sgp4.api import Satrec, WGS72
from skyfield.elementslib import osculating_elements_of

from common import *

os.system("go build -buildmode=c-shared -o ./go_fit.so .")


def fitness_no_sim(satellites, possible, real_sat_grid):

    Ticcer = TicToc()
    # Ticcer.tic()
    library = ctypes.cdll.LoadLibrary("./go_fit.so")
    conn1 = library.consensus_completeness_per_non_ga
    conn1.restype = ctypes.POINTER(ctypes.c_int)

    conn1.argtypes = [
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_int64,
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_int64,
        ctypes.c_int64,
        ctypes.POINTER(ctypes.c_int)
    ]
    
    # Ticcer.tic()
    sizer = len(real_sat_grid)
    grid_raw = real_sat_grid.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    # print("To ctype conversion")
    # Ticcer.toc()

    num_sats = int(len(satellites))

    possible_1 = array('d', (possible).flatten().tolist())
    possible_raw = (ctypes.c_double * len(possible_1)).from_buffer(possible_1)

    size = ctypes.c_int()

    # Ticcer.tic()
    c = conn1(possible_raw, len(possible_raw), grid_raw, sizer, num_sats, ctypes.byref(size))

    return [c[i] for i in range(size.value)]




def get_possible(satellites):
    possible = np.array(list(itertools.combinations(np.arange(0,len(satellites)), 4)))
    return possible



def build_grid(satellites, time):
    big_comb = np.array(satellites)

    real_sat_grid = np.zeros((len(big_comb), len(big_comb), len(time)))
    real_sat_grid[real_sat_grid == 0] = -1

    for i in tqdm(range(len(big_comb)), desc="Generate real satellite's interactions"):
        for j in range(len(big_comb)):
            if i != j:
                x = np.where((big_comb[i].at(time) - big_comb[j].at(time)).distance().km <= 500)[0]
                real_sat_grid[i,j,:len(x)] = x
                real_sat_grid[j,i,:len(x)] = x

    return real_sat_grid


def gen_sat(val):
    argp_i = val["argp_i"]
    ecc_i = val["ecc_i"]
    inc_i = val["inc_i"]
    raan_i = val["raan_i"]
    anom_i = val["anom_i"]
    mot_i = val["mot_i"]
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
    return sim_sat

def flattener(real_sat_grid):

        flat_grid = []
        for i in range(np.shape(real_sat_grid)[0]):
            for j in range(np.shape(real_sat_grid)[1]):
                flat_grid.extend(real_sat_grid[i,j])

        return flat_grid

open_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(open_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)

json_out = {}

for yyy in range(0,10):
    data1 = []
    for xxx in range(1,11):
        temp = []
        ts = load.timescale()

        start_date = datetime.datetime(2024,9,11+yyy, tzinfo=utc)
        end_date = start_date + relativedelta(days=xxx/10)
        time_range = date_range(start_date, end_date, 30, 'seconds')
        time = ts.from_datetimes(time_range)
        epoch = (start_date - datetime.datetime(1949,12,31,0,0, tzinfo=utc))

        satellites = get_icsmd_satellites(open_location+"/active.tle", "icsmd_sats.txt")

        
        print("Number of days:", xxx/10)

        real_sat_grid = build_grid(satellites, time)
        possible = get_possible(satellites)
        flat_sat_grid = np.array(flattener(real_sat_grid), dtype=float)
        
        completed_no_sim = fitness_no_sim(satellites, possible, flat_sat_grid)
        print(completed_no_sim)
        temp.append([completed_no_sim, 79])

        # print(completed_no_sim/(len(possible)*4))



        val = {
            "argp_i": -86.92099170309598,
            "ecc_i": 0.07186028590257361,
            "inc_i": 79.86642516462781,
            "raan_i": 147.3944794086328,
            "anom_i": 19.969317660223894,
            "mot_i": 6144.856529157008
        }
        sim_sat = gen_sat(val)
        satellites = [sim_sat, *satellites]

        real_sat_grid = build_grid(satellites, time)
        possible = get_possible(satellites)
        flat_sat_grid = np.array(flattener(real_sat_grid), dtype=float)
        
        completed_with_sim = fitness_no_sim(satellites, possible, flat_sat_grid)
        print(completed_with_sim)
        temp.append([completed_with_sim, 80])

        data1.append(temp)

        # print(completed_with_sim/(len(possible)*4))
        print(data1)
    json_out.update({"day_"+str(yyy): data1})

    save_json("with_without.json", json_out)

save_json("with_without.json", json_out)


