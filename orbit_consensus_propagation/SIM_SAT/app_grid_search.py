import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import itertools 
import datetime
from functools import reduce

from dateutil.relativedelta import relativedelta
from skyfield.api import load, utc
from skyfield.iokit import parse_tle_file
from skyfield.elementslib import osculating_elements_of

import ctypes
from array import array

from common import *
from ga_func import *


########### Setup data paths


open_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(open_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)


######### Get date and times for analysis

ts = load.timescale()

start_date = datetime.datetime(2024,9,11, tzinfo=utc)
end_date = start_date + relativedelta(days=0.1)
time_range = date_range(start_date, end_date, 30, 'seconds')
time = ts.from_datetimes(time_range)
epoch = (start_date - datetime.datetime(1949,12,31,0,0, tzinfo=utc))


########### Get orbital elements of all sats


satellites = get_satellites(open_location+"/active.tle")

print('Loaded', len(satellites), 'satellites')

all_starts = []
all_params = []
for sat in satellites:
    barycentric = sat.at(ts.from_datetime(start_date))

    orbit_elements = osculating_elements_of(barycentric)

    temp = []
    temp.append(orbit_elements.argument_of_periapsis.degrees)
    temp.append(orbit_elements.eccentricity)
    temp.append(orbit_elements.inclination.degrees)
    temp.append(orbit_elements.longitude_of_ascending_node.degrees)
    temp.append(orbit_elements.mean_anomaly.degrees)
    temp.append(orbit_elements.mean_motion_per_day.degrees)
    all_params.append(temp)

all_params = np.array(all_params)

all_params_mean = np.nanmean(all_params,axis=0)
all_params_std = np.nanstd(all_params,axis=0)
all_params_min = all_params_mean - 3*all_params_std
all_params_max = all_params_mean + 3*all_params_std


############## Get icmsd satellites


# satellites = get_icsmd_satellites(open_location+"/active.tle", "icsmd_sats.txt")
satellites = get_satellites(open_location+"/active.tle", refine_by_name="icsmd_sats.txt")


#############


combinati = itertools.combinations(["argp","ecc","inc","raan","anom","mot"],2)

quality = 25

num_participants = 4

os.system("go build -buildmode=c-shared -o ./go_fit.so .")



################## Pre-Generate real satellite interaction grid ##################

big_comb = np.array(satellites)
real_sat_grid = np.zeros((len(big_comb), len(big_comb), len(time)))
real_sat_grid[real_sat_grid == 0] = -1
gg = []
for i in tqdm(range(len(big_comb)), desc="Generate real satellite's interactions"):
    for j in range(len(big_comb)):
        if i != j:
            x = np.where((big_comb[i].at(time) - big_comb[j].at(time)).distance().km <= 500)[0]
            real_sat_grid[i,j,:len(x)] = x
            real_sat_grid[j,i,:len(x)] = x
            if len(x) > 0:# and j > i:
                gg.append([i+1,j+1])

for i in range(len(satellites)):
    gg.append([0,i+1])
gg = np.array(gg)

################## Combination builder ##################

# Creates possible combinations from satellites that can see each other
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
combs_arr = array('d', (possible).flatten().tolist())
combs_raw = (ctypes.c_double * len(combs_arr)).from_buffer(combs_arr)
print("Possible satellite consensus combinations:", np.shape(possible))


real_sat_grid_flat = np.array(flatten_plus_one(real_sat_grid, time), dtype=float)
depth = np.shape(real_sat_grid)[2]

for comb in (list(combinati)):
    if "argp" in comb:
        argp = np.linspace(-180, 180, quality)
    else:
        argp = np.linspace(-180, 180, 5)
        # argp = [all_params_mean[0]]
    if "ecc" in comb:
        ecc = np.linspace(0, all_params_max[1], quality)
    else:
        ecc = np.linspace(0, all_params_max[1], 5)
        # ecc = [all_params_mean[1]]
    if "inc" in comb:
        inc = np.linspace(-90, 90, quality)
    else:
        inc = np.linspace(-90, 90, 5)
        # inc = [all_params_mean[2]]
    if "raan" in comb:
        raan = np.linspace(-180, 180, quality)
    else:
        raan = np.linspace(-180, 180, 5)
        # raan = [all_params_mean[3]]
    if "anom" in comb:
        anom = np.linspace(-180, 180, quality)
    else:
        # anom = np.linspace(-180, 180, 1)
        anom = [all_params_mean[4]]
    if "mot" in comb:
        mot = np.linspace(4000, 6500, quality)
    else:
        mot = np.linspace(4000, 6500, 5)
        # mot = [all_params_mean[5]]


    all_elements = [argp, ecc, inc, raan, anom, mot]

    out_data = np.zeros((len(argp),len(ecc),len(inc),len(raan),len(anom),len(mot)))

    save_json(save_location+"/details_"+comb[0]+"_"+comb[1]+".json", {
        "argp": np.array(argp).tolist(),
        "ecc": np.array(ecc).tolist(),
        "inc": np.array(inc).tolist(),
        "raan": np.array(raan).tolist(),
        "anom": np.array(anom).tolist(),
        "mot": np.array(mot).tolist(),
    })

    id_product = itertools.product(
        np.arange(len(argp)),
        np.arange(len(ecc)),
        np.arange(len(inc)),
        np.arange(len(raan)),
        np.arange(len(anom)),
        np.arange(len(mot))
    )

    for i1, i2, i3, i4, i5, i6 in tqdm(list(id_product)):
        X = {
            "argp_i": argp[i1],
            "ecc_i": ecc[i2],
            "inc_i": inc[i3],
            "raan_i": raan[i4],
            "anom_i": anom[i5],
            "mot_i": mot[i6]
        }
        sim_sat = make_satellite(X, epoch, ts)

        completed = fitness(sim_sat, satellites, combs_raw, real_sat_grid_flat.copy(), depth, time, num_participants)

        out_data[i1,i2,i3,i4,i5,i6] = len(completed)

    np.save(save_location+"/contact_num_"+comb[0]+"_"+comb[1], out_data)














