import os
import numpy as np
import datetime
from tqdm import tqdm
import itertools 
from functools import reduce


from skyfield.api import load, EarthSatellite
from skyfield.iokit import parse_tle_file
from skyfield.elementslib import osculating_elements_of
from sgp4.api import Satrec, WGS72

import ctypes
from array import array

from common import *
from ga_func import *

open_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(open_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data-animation")
if not os.path.exists(save_location):
    os.makedirs(save_location)

number_of_start_days = 10

os.system("go build -buildmode=c-shared -o ./go_fit.so .")

ts = load.timescale()













def fitness_no_sim(satellites, possible, real_sat_grid, num_participants=4):

    library = ctypes.cdll.LoadLibrary("./go_fit.so")
    conn1 = library.consensus_completeness_per
    conn1.restype = ctypes.POINTER(ctypes.c_int)

    conn1.argtypes = [
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_int64,
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_int64,
        ctypes.c_int64,
        ctypes.c_int64,
        ctypes.POINTER(ctypes.c_int)
    ]
    
    sizer = len(real_sat_grid)
    grid_raw = real_sat_grid.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

    num_sats = int(len(satellites))

    possible_1 = array('d', (possible).flatten().tolist())
    possible_raw = (ctypes.c_double * len(possible_1)).from_buffer(possible_1)

    size = ctypes.c_int()

    c = conn1(possible_raw, len(possible_raw), grid_raw, sizer, num_sats, num_participants, ctypes.byref(size))

    return [c[i] for i in range(size.value)]




def build_grid(satellites, time, num_participants=4):
    big_comb = np.array(satellites)
    real_sat_grid = np.zeros((len(big_comb), len(big_comb), len(time)))
    real_sat_grid[real_sat_grid == 0] = -1
    gg = []
    for i in range(len(big_comb)):
        for j in range(len(big_comb)):
            if i != j:
                x = np.where((big_comb[i].at(time) - big_comb[j].at(time)).distance().km <= 500)[0]
                real_sat_grid[i,j,:len(x)] = x
                real_sat_grid[j,i,:len(x)] = x
                if len(x) > 0:# and j > i:
                    gg.append([i,j])

    # for i in range(len(satellites)):
    #     gg.append([0,i+1])
    gg = np.array(gg)

    pos_last = gg.copy()
    while np.shape(pos_last)[1] < num_participants:
        pos = pos_last.copy()
        pos_last = []
        for item in pos:
            x_vals = []
            for itemx in item:
                x_vals.append(np.unique(np.append(gg[gg[:,0] == itemx, 1], gg[gg[:,1] == itemx, 0])))
            for x in reduce(np.intersect1d, x_vals):
                pos_last.append([*item, x])

    possible = np.array(pos_last)

    return real_sat_grid, possible





out_data = []
for day_number in tqdm(range(number_of_start_days)):

    start_date = datetime.datetime(2024,9,11+day_number, tzinfo=utc)
    epoch = (start_date - datetime.datetime(1949,12,31,0,0, tzinfo=utc))

    global_frame_data = []

    current_out = {}
    for time_frame in [0.1,0.5,1]:

        file_name = "data-ga/participants_4_startday_{:02d}".format(int(day_number))
        file_name += "_conntime_{:02d}.json".format(int(round(time_frame*10)))
        dataset = load_json(file_name)
        val = dataset[-1]["x"][np.argmin(dataset[-1]["f"])]

        del dataset
        sim_sat = make_satellite(val, epoch, ts)

        satellites = get_satellites(open_location+"/active.tle", refine_by_name="icsmd_sats.txt")

        satellites2 = [sim_sat, *satellites]

        end_date = start_date + relativedelta(days=time_frame)
        time_range = date_range(start_date, end_date, 30, 'seconds')
        time = ts.from_datetimes(time_range)


        real_sat_grid, possible = build_grid(satellites, time)

        flat_sat_grid = np.array(flattener(real_sat_grid), dtype=float)

        completed_no_sim = fitness_no_sim(satellites, possible, flat_sat_grid)

        real_sat_grid, possible2 = build_grid(satellites2, time)

        flat_sat_grid2 = np.array(flattener(real_sat_grid), dtype=float)

        completed_with_sim = fitness_no_sim(satellites2, possible2, flat_sat_grid2)

        current_out.update({
            str(time_frame): {
                "no_sim": {
                    "num_participants": len(completed_no_sim),
                    "participants": np.array(completed_no_sim).tolist()
                },
                "with_sim": {
                    "num_participants": len(completed_with_sim),
                    "participants": np.array(completed_with_sim).tolist()
                },
                "best_sim_stats": val
            }
        })
    out_data.append(current_out)

save_json("raw_results.json", out_data)