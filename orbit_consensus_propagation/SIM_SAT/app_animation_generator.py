import os
import numpy as np
import datetime
from tqdm import tqdm
import itertools 
from functools import reduce
from pytictoc import TicToc


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
timesteps = 25

os.system("go build -buildmode=c-shared -o ./go_fit.so .")

ts = load.timescale()

satellites = get_satellites(open_location+"/active.tle", refine_by_name="icsmd_sats.txt")



Ticcer = TicToc()







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
    # gg = []
    for i in tqdm(range(len(big_comb)), desc="Build grid"):
        for j in range(len(big_comb)):
            if i != j:
                x = np.where((big_comb[i].at(time) - big_comb[j].at(time)).distance().km <= 500)[0]
                real_sat_grid[i,j,:len(x)] = x
                real_sat_grid[j,i,:len(x)] = x

    possible = np.array(list(itertools.combinations(np.arange(0,len(satellites)), 4)))

    return real_sat_grid, possible






for day_number in range(number_of_start_days):

    start_date = datetime.datetime(2024,9,11+day_number, tzinfo=utc)
    end_date = start_date + relativedelta(days=0.1)
    time_range = date_range(start_date, end_date, 30, 'seconds')
    time = ts.from_datetimes(time_range)

    real_sat_grid_og, possible = build_grid(satellites, time)

    stacker_no_sim = []
    for frame in tqdm(np.linspace(0,24*60*0.1,timesteps), desc="Sim day "+str(day_number)+" | No sim gen"):

        if frame > 0:
            real_sat_grid = real_sat_grid_og.copy()
            real_sat_grid[real_sat_grid > frame*2] = -1
            while np.all(real_sat_grid[:,:,-1] == -1):
                real_sat_grid = real_sat_grid[:,:,:-1]
            flat_sat_grid = np.array(flattener(real_sat_grid), dtype=float)

            completed_no_sim = fitness_no_sim(satellites, possible, flat_sat_grid)
        else:
            completed_no_sim = []
        
        stacker_no_sim.append(completed_no_sim)


    for start_day in [0,1,2,3,4,5,6,7,8,9,"special", "special2"]:
        if start_day == "special" or start_day == "special2":
            file_name = "data-ga/participants_4_startday_"+start_day+"_conntime_01.json"
            gen_date = datetime.datetime(2024,9,11, tzinfo=utc)
        else:
            file_name = "data-ga/participants_4_startday_{:02d}_conntime_01.json".format(int(start_day))
            gen_date = datetime.datetime(2024,9,11+start_day, tzinfo=utc)
        epoch = (gen_date - datetime.datetime(1949,12,31,0,0, tzinfo=utc))
        dataset = load_json(file_name)
        val = dataset[-1]["x"][np.argmin(dataset[-1]["f"])]
        del dataset
        sim_sat = make_satellite(val, epoch, ts)

        satellites2 = [sim_sat, *satellites]

        global_frame_data = []


        real_sat_grid_og_2, possible2 = build_grid(satellites2, time)

        for i, frame in enumerate(tqdm(np.linspace(0,24*60*0.1,timesteps), desc="Sim day "+str(day_number)+" | Opt day "+str(start_day))):

            if frame > 0:

                real_sat_grid_2 = real_sat_grid_og_2.copy()
                real_sat_grid_2[real_sat_grid_2 > frame*2] = -1
                while np.all(real_sat_grid_2[:,:,-1] == -1):
                    real_sat_grid_2 = real_sat_grid_2[:,:,:-1]
                flat_sat_grid_2 = np.array(flattener(real_sat_grid_2), dtype=float)

                completed_with_sim = fitness_no_sim(satellites2, possible2, flat_sat_grid_2)

            else:
                completed_with_sim = []
        

            all_starts_no_sim = []
            for sat in satellites:
                barycentric = sat.at(ts.utc(2024, 9, 11+day_number, 0, frame, 0))
                all_starts_no_sim.append(barycentric.position.km)

            all_starts_no_sim = np.array(all_starts_no_sim)

            barycentric = satellites2[0].at(ts.utc(2024, 9, 11+day_number, 0, frame, 0))
            all_starts_with_sim = barycentric.position.km

            all_starts_with_sim = np.array(all_starts_with_sim)
        

            global_frame_data.append({
                "time_minutes": frame,
                "completed_no_sim": stacker_no_sim[i],
                "completed_with_sim": completed_with_sim,
                "position_no_sim": all_starts_no_sim.tolist(),
                "position_of_sim": all_starts_with_sim.tolist(),
            })

            # if frame%100 == 0:
            #     save_json(save_location+"/animation_data_optday_"+str(start_day)+"_proccessday_"+str(day_number)+".json", global_frame_data)


        save_json(save_location+"/animation_data_optday_"+str(start_day)+"_proccessday_"+str(day_number)+".json", global_frame_data)
