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


data_types = ["Inclination", "RAAN", "Eccentricity", "Arg of Peri", "Mean Motion"]

data = []
data_x = []

li_inc=[]
li_raan=[]
li_e=[]
li_ap=[]
li_n=[]

for i in range(len(li_sat_names)):
    current_sat = sat_name_to_kepler(li_sat_names[i])
    tle_rec = ephem.readtle(current_sat["name"], current_sat["line1"], current_sat["line2"]);
    tle_rec.compute()
    li_inc.append(tle_rec.inc)
    li_raan.append(tle_rec.raan)
    li_e.append(tle_rec.e)
    li_ap.append(tle_rec.ap)
    li_n.append(tle_rec.n)
    data_x.append([1, 2, 3, 4, 5])

li_inc = np.array(li_inc)
li_raan = np.array(li_raan)
li_e = np.array(li_e)
li_ap = np.array(li_ap)
li_n = np.array(li_n)

li_e = np.log10(li_e)

average_vals = [np.average(li_inc),  np.average(li_raan), np.average(li_e),
                np.average(li_ap), np.average(li_n)]
min_vals = [np.amin(li_inc),  np.amin(li_raan), np.amin(li_e),
                np.amin(li_ap), np.amin(li_n)]
max_vals = [np.amax(li_inc),  np.amax(li_raan), np.amax(li_e),
                np.amax(li_ap), np.amax(li_n)]


# std_vals = np.array([np.std(li_inc),  np.std(li_raan), np.std(li_e),
#                 np.std(li_ap), np.std(li_n)])
# min_percentile = np.array(average_vals)-(2*std_vals)
# max_percentile = np.array(average_vals)+(2*std_vals)


fig = plt.figure(figsize=[15, 10])

def scale_y(y_in):
    y_out = y_in
    # Inclination
    y_out[0] = (y_out[0]-min_vals[0])/(max_vals[0]-min_vals[0])
    # RAAN
    y_out[1] = (y_out[1]-min_vals[1])/(max_vals[1]-min_vals[1])
    # Eccentricity
    y_out[2] = (y_out[2]-min_vals[2])/(max_vals[2]-min_vals[2]) #(0.5*average_vals[2]-min_vals[2])
    # Argument of Periapsis
    y_out[3] = (y_out[3]-min_vals[3])/(max_vals[3]-min_vals[3])
    # Mean Motion
    y_out[4] = (y_out[4]-min_vals[4])/(max_vals[4]-min_vals[4])
    return y_out


colors = plt.cm.plasma(np.linspace(0,1,len(li_sat_names)))

math_const = np.amax(li_unique)-np.amin(li_unique)
min_const = np.amin(li_unique)

# for i in range(len(li_sat_names)):
#     data_y = [li_inc[i], li_raan[i], li_e[i], li_ap[i], li_n[i]]
#     current_colour = len(li_sat_names)*(li_unique[i]-min_const)/math_const
#     # print(round(current_colour))
#     plt.plot(data_types, scale_y(data_y), color=colors[round(current_colour)-1], alpha=(1/(i+1)))
#     plt.scatter([i*4/(len(li_sat_names))], [0.2], c=[li_unique[i]], cmap="plasma")

for i in range(len(li_sat_names)):
    data_y = [li_inc[i], li_raan[i], li_e[i], li_ap[i], li_n[i]]
    current_colour = len(li_sat_names)*(li_unique[i]-np.amin(li_unique))/(np.amax(li_unique)-np.amin(li_unique))
    # print(round(current_colour))
    plt.plot(data_types, scale_y(data_y), color=colors[round(current_colour)-1], alpha=0.05)
    

print()

plt.xlim([0, 4])
plt.ylim([0, 1])

min_max_vals = [np.amin(li_unique), np.amax(li_unique)]

plt.scatter([-1, -1], [-1, -1], c=min_max_vals, cmap="plasma")
plt.colorbar()
# fig.set_facecolor('black')
# plt.legend()
# plt.axis('equal')
plt.savefig("distribution_against_elements.png")
# plt.show()
plt.show()
