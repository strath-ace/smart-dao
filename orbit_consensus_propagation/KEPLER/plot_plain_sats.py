# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import os
import json
import ephem
import numpy as np
import math
from datetime import datetime
from py_lib.generic import *
from py_lib.get_less_sats import reduce_sats
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.pyplot as plt

######### INPUT PARAMS

IMAGE_DIR = "temp"

file_names = "data_plain_sats"

chosen_dis = 0  # Column 0 in all_combs


######### Graph Sizes

x_axis_size = 30
y_axis_size = 30
colorbar_size = 30
title_size = 40
legend_size = 30

#########

def flatten(matrix):
    return [item for row in matrix for item in row]


save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_names)
if not os.path.exists(save_location):
    os.makedirs(save_location)
image_location = os.path.join(save_location, IMAGE_DIR)
if not os.path.exists(image_location):
    os.makedirs(image_location)

data_all_sats = load_json(save_location+"/sorted_sats.json")

data_icsmd_sats = load_json(save_location+"/sorted_sats_icsmd.json")


#####

kepler_li = []
for sat_data in data_all_sats:
    sat = ephem.readtle(sat_data["name"], sat_data["line1"], sat_data["line2"])
    if sat.n < 16 and sat.n > 11.25 and sat.e < 0.25:
        kepler_li.append([sat.inc, sat.raan, sat.e, sat.ap, sat.n, sat.M])
kepler_li = np.array(kepler_li)

kepler_li2 = []
for sat_data in data_icsmd_sats:
    sat = ephem.readtle(sat_data["name"], sat_data["line1"], sat_data["line2"])
    # if sat.n < 16 and sat.n > 11.25 and sat.e < 0.25:
    kepler_li2.append([sat.inc, sat.raan, sat.e, sat.ap, sat.n, sat.M])
kepler_li2 = np.array(kepler_li2)


############ Plotting

title_names = ["Inclination", "RAAN", "Eccentricity", "Argument of Periapsis", "Mean Motion", "Mean Anomaly"]
data_types = ["Inclination (Degrees)", "RAAN (Degrees)", "Eccentricity", "Arg of Peri (Degrees)", "Mean Motion (per day)", "Mean anomaly (Degrees)"]
file_types = ["inclination", "raan", "eccentricity", "arg_of_peri", "mean_motion", "mean_anomaly"]

cmap_val = matplotlib.colormaps.get_cmap('plasma')

# print(np.shape(conns), np.shape(kepler_li[:,element]))

proper_set = [0,1,2,3,4,5]

for element1 in proper_set:
    for element2 in proper_set:
        if element1 != element2:
            fig, axs = plt.subplots(figsize=(20,30))
            plt.title(title_names[element1]+" vs "+title_names[element2], fontsize=title_size)
            plt.xlabel(data_types[element1], fontsize=x_axis_size)
            plt.ylabel(data_types[element2], fontsize=y_axis_size)
            plt.scatter(kepler_li[:,element1], kepler_li[:,element2])
            plt.scatter(kepler_li2[:,element1], kepler_li2[:,element2])
            plt.tick_params(axis='both', which='major', labelsize=colorbar_size)
            if element1 == 2:
                plt.xscale("log")
            if element2 == 2:
                plt.yscale("log")
            plt.savefig(image_location+"/"+file_types[element1]+"_"+file_types[element2]+".png")
            plt.clf()



# proper_set = [0,2,4]

# for element1 in proper_set:
#     for element2 in proper_set:
#         if element1 != element2:
#             fig, axs = plt.subplots(figsize=(30,30))
#             plt.title("Cross "+title_names[element1]+" vs "+title_names[element2], fontsize=title_size)
#             plt.xlabel(data_types[element1], fontsize=x_axis_size)
#             plt.ylabel(data_types[element2], fontsize=y_axis_size)

#             x_vals = np.unique(kepler_li[:,element1])
#             y_vals = np.unique(kepler_li[:,element2])

#             # Change first in each to x_vals
#             GRID = np.zeros((len(y_vals), len(x_vals)))
#             GRID.fill(float('nan'))
#             GRID_DIVIDE = np.zeros((len(y_vals), len(x_vals)))

#             for i, x in enumerate(x_vals):
#                 for ii, y in enumerate(y_vals):
#                     for iii in range(len(kepler_li)):
#                         if opt1 and kepler_li[iii,element1] == x and kepler_li[iii,element2] == y and conns[iii] !=0:
#                             if math.isnan(GRID[ii,i]):
#                                 GRID[ii,i] = 0
#                             GRID[ii, i] += conns[iii]
#                             GRID_DIVIDE[ii,i] += 1
#                         if opt2 and kepler_li[iii,element1] == x and kepler_li[iii,element2] == y:
#                             if math.isnan(GRID[ii,i]):
#                                 GRID[ii,i] = 0
#                             GRID[ii, i] += conns[iii]
#                             GRID_DIVIDE[ii,i] += 1

#             for i in range(len(GRID)):
#                 for ii in range(len(GRID[0])):
#                     if not math.isnan(GRID[i,ii]):
#                         GRID[i,ii] = GRID[i,ii] / GRID_DIVIDE[i,ii]            
            
#             X,Y = np.meshgrid(x_vals, y_vals)
#             # print(GRID)
#             GRID = np.ma.array(GRID, mask=np.isnan(GRID))
#             # print(GRID)
#             plt.contourf(X, Y, GRID, levels=np.linspace(0,np.amax(GRID), round(np.amax(GRID))-1), vmin=0, vmax=np.amax(GRID))
#             plt.tick_params(axis='both', which='both', labelsize=colorbar_size)
#             cbar = plt.colorbar()
            
#             cbar.ax.tick_params(labelsize=colorbar_size) 
#             plt.savefig(image_location+"/"+"cross_"+file_types[element1]+"_vs_"+file_types[element2]+".png")
#             plt.clf()
















# element1 = 2
# element2 = 4
# fig, axs = plt.subplots(figsize=(30,30))
# plt.title("Mixed", fontsize=title_size)
# plt.xlabel(data_types[element1], fontsize=x_axis_size)
# plt.ylabel(data_types[element2], fontsize=y_axis_size)



# x_vals = kepler_li[:,element1].copy()
# y_vals = kepler_li[:,element2].copy()
# conns2 = conns.copy()
# # np.append(x_vals, 0)
# # np.append(y_vals, 0)
# # np.append(conns2, 0)
# plt.tricontour(x_vals, y_vals, conns2, 100, linewidths=0, colors='k')
# plt.tricontourf(x_vals, y_vals, conns2, 100)
# plt.scatter([0],[0], c=0, vmin=0, vmax=num_sats)
# # plt.yscale("log")
# plt.tick_params(axis='both', which='both', labelsize=colorbar_size)
# cbar = plt.colorbar()

# cbar.ax.tick_params(labelsize=colorbar_size) 
# plt.savefig(image_location+"/"+"mixed_plot"+".png")
# # plt.ylim([600000, 999999])
# plt.yscale("log")
# plt.savefig(image_location+"/"+"mixed_plot_logged"+".png")
# plt.clf()