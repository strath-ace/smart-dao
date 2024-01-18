import matplotlib.pyplot as plt
import numpy as np
import ctypes
import json
import os
import csv
from math import ceil
from matplotlib.ticker import MaxNLocator
import math
import ephem
from matplotlib.collections import LineCollection

# Opens go code
import ctypes
library = ctypes.cdll.LoadLibrary('./combine.so')
combine = library.combine
combine()

print("Graphing Data")

input_file = "graph_data.csv"

# Create save location if not already exist
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)
# Create save location if not already exist
upper_location = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", "..", "data")
if not os.path.exists(upper_location):
    os.makedirs(upper_location)
def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output
config = load_json(save_location+"/all_conns_config.json")
def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            try:
                temp = []
                for item in row:
                    temp.append(eval(row))
                output.append(temp)
            except:
                try:
                    output.append(eval(row))
                except:
                    try:
                        output.append(row)
                    except:
                        output = row    
    f.close()
    return output
li_all = csv_input(save_location+"/"+input_file)
li_all = np.rot90(np.array(li_all))
# Sort by li_nums[:,0] first then by li_num[:,1] (aka sort by unique then total)
ind = np.lexsort((li_all[:,1], li_all[:,2]), axis=0)
li_nums = np.asanyarray(li_all[:,1:], dtype=float)
li_sat_names = [li_all[:,0][i] for i in ind]
li_count = [li_nums[:,0][i] for i in ind]
li_unique = [li_nums[:,1][i] for i in ind]


all_tle_data = load_json(save_location+"/leo_sats_parsed.json")

def sat_name_to_kepler(sat_name):
    for i in range(len(all_tle_data)):
        if all_tle_data[i]["name"] == sat_name:
            return all_tle_data[i]
    return "ERROR"

max_params = []




data = []
data_x = []

li_inc=[]
li_raan=[]
li_e=[]
li_ap=[]
li_n=[]
li_omega=[]

for i in range(len(li_sat_names)):
    current_sat = sat_name_to_kepler(li_sat_names[i])
    tle_rec = ephem.readtle(current_sat["name"], current_sat["line1"], current_sat["line2"]);
    tle_rec.compute()
    li_inc.append(tle_rec.inc)
    li_raan.append(tle_rec.raan)
    li_e.append(tle_rec.e)
    li_ap.append(tle_rec.ap)
    li_n.append(tle_rec.n)
    li_omega.append(tle_rec.M)
    data_x.append([1, 2, 3, 4, 5, 6])

li_inc = np.array(li_inc)
li_raan = np.array(li_raan)
li_e = np.array(li_e)
li_ap = np.array(li_ap)
li_n = np.array(li_n)

li_e = np.log10(li_e)

big_data = [li_inc, li_raan, li_e, li_ap, li_n, li_omega]

fig, axs = plt.subplots(nrows=1, ncols=6, figsize=(30, 10))

data_types = ["Inclination (Degrees)", "RAAN (Degrees)", "Eccentricity (Log10(Degrees))", "Arg of Peri (Degrees)", "Mean Motion (per day)", "Mean anomaly (Degrees)"]

clusters = [1, 2, 3, 4, 5]

group = [[0,1403], [1403,2936], [2936,3974], [3974,7691], [7691, len(li_sat_names)]]

for j in range(len(data_types)):
    data = []
    for clus in group:
        temp = []
        for i in range(clus[0], clus[1]):
            temp.append(big_data[j][i])
        data.append(temp)

    axs[j].set_title(data_types[j])
    axs[j].violinplot(data, clusters, points=100, widths=0.8,
                        showmeans=False, showextrema=False, showmedians=False)




# plt.legend()
# plt.axis('equal')
plt.savefig("distribution_for_element1_violin.png")
# plt.show()
plt.show()
