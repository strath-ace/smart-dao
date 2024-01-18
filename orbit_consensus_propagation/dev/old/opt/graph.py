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
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection

print("Graphing Data")


# Create save location if not already exist
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
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

all_tle_data = load_json("sorted_sats.json")



# def sat_name_to_kepler(sat_name):
#     for i in range(len(all_tle_data)):
#         if all_tle_data[i]["name"] == sat_name:
#             return all_tle_data[i]
#     return "ERROR"

max_params = []




data = []
data_x = []

li_inc=[]
li_raan=[]
li_e=[]
li_ap=[]
li_n=[]
li_omega=[]

for sat in all_tle_data:
    tle_rec = ephem.readtle(sat["name"], sat["line1"], sat["line2"]);
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

clusters = [1, 2]

group = [[39, 78, 49, 35], np.asarray((np.linspace(0,len(all_tle_data)-1, len(all_tle_data))), dtype=(int)) ]

np.random.seed(seed=1238935)

label_list = ["46.6 hour consensus", "all sats"]
colours = np.random.rand(len(clusters),3)

labels = []
for i, _ in enumerate(clusters):
    labels.append((mpatches.Patch(color=colours[i]), label_list[i]))

def add_label(violin):
    for i, pc in enumerate(violin["bodies"]):
        pc.set_facecolor(colours[i])
        pc.set_alpha(1)
        
for j in range(len(data_types)):
    data = []
    for clus in group:
        temp = []
        for i in clus:
            temp.append(big_data[j][i])
            
        data.append(temp)

    axs[j].set_title(data_types[j])
    add_label(axs[j].violinplot(data, clusters, points=100, widths=0.4,
                        showmeans=False, showextrema=False, showmedians=False))

plt.legend(*zip(*labels), loc=2)
# plt.axis('equal')
plt.savefig("distribution_for_element_violin.png")
# plt.show()
plt.show()
