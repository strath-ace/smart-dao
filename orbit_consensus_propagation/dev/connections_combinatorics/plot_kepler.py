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

######### INPUT PARAMS

IMAGE_DIR = "kepler"

file_names = ["data_all", "data_icsmd"]
name_names = ["All", "ICSMD"]
bins_num = [20, 10]
point_li = [100, 20]

chosen_dis = 0  # Row 2 in all_combs

######### Graph Sizes

x_axis_size = 30
y_axis_size = 30
colorbar_size = 30
title_size = 40
legend_size = 30

#########

def flatten(matrix):
    return [item for row in matrix for item in row]

for j in range(len(file_names)):

    save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_names[j])
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    image_location = os.path.join(save_location, IMAGE_DIR)
    if not os.path.exists(image_location):
        os.makedirs(image_location)

    data_all_sats = load_json(save_location+"/sorted_sats.json")
    num_sats = len(data_all_sats)
    start_time = round(load_json(save_location+"/dataset.json")["timestamp"])

    all_combs = np.asarray(csv_input(save_location+"/all_combs.csv"), dtype="float64")
    all_combs = np.rot90(all_combs)

    #####

    all_sats = []
    for sat_data in data_all_sats:
        all_sats.append(ephem.readtle(sat_data["name"], sat_data["line1"], sat_data["line2"]))

    kepler_li = []
    for order, sat in enumerate(all_sats):
        sat.compute(datetime.fromtimestamp(start_time))
        kepler_li.append([sat.inc, sat.raan, np.log10(sat.e), sat.ap, sat.n, sat.M])
    kepler_li = np.array(kepler_li)

    conns = all_combs[chosen_dis]

    num_bins = bins_num[j]
    bins = np.linspace(0, np.amax(conns), num_bins)

    conns_bin = np.digitize(conns, bins)

    binned_kepler = []
    for i in range(num_bins):
        binned_kepler.append([])
    for i, binn in enumerate(conns_bin):
        binned_kepler[binn-1].append(kepler_li[i])

    for i in range(num_bins):
        print(len(binned_kepler[i]))

    ############ Plotting
    
    title_names = ["Inclination", "RAAN", "Eccentricity", "Argument of Periapsis", "Mean Motion", "Mean Anomaly"]
    data_types = ["Inclination (Degrees)", "RAAN (Degrees)", "Eccentricity (Log10(Degrees))", "Arg of Peri (Degrees)", "Mean Motion (per day)", "Mean anomaly (Degrees)"]
    file_types = ["inclination", "raan", "eccentricity", "arg_of_peri", "mean_motion", "mean_anomaly"]
    
    cmap_val = matplotlib.colormaps.get_cmap('plasma')
    norm = matplotlib.colors.Normalize(vmin=0, vmax=num_sats)
    
    for element in range(6):
        fig, axs = plt.subplots(figsize=(20,30))
        plt.scatter([0], [0], c=0, cmap="plasma", vmin=0, vmax=num_sats, alpha=1)
        cbar = plt.colorbar()
        cbar.ax.tick_params(labelsize=colorbar_size) 
        plt.title(title_names[element], fontsize=title_size)
        plt.xlabel("Number of connections", fontsize=x_axis_size)
        plt.ylabel(data_types[element], fontsize=y_axis_size)
        plt.tick_params(axis='both', which='major', labelsize=colorbar_size)
        max_temp_len = 0
        clusters = []
        data = []
        for x in range(num_bins):
            temp = []
            for y in range(len(binned_kepler[x])):
                temp.append(binned_kepler[x][y][element])
            if len(temp) > 0:
                if len(temp) > max_temp_len:
                    max_temp_len = len(temp)
                clusters.append((x*num_sats/num_bins)+(0.5*num_sats/num_bins))
                data.append(temp)

        mean_val = []
        weight = []
        for x in range(len(data)):
            violin = plt.violinplot([data[x]], [clusters[x]], points=len(data[x]), widths=1*(num_sats/num_bins)*math.cbrt(len(data[x])/max_temp_len),
                    showmeans=False, showextrema=False, showmedians=False)
            violin["bodies"][0].set_facecolor(cmap_val(norm(clusters[x])))
            violin["bodies"][0].set_alpha(0.9)
            mean_val.append(np.mean(data[x]))
            weight.append(np.cbrt(len(data[x])))
        
        
        # Plot True Mean
        # plt.plot(clusters, mean_val, c="black", label="Mean")
        # Plot Smoothed Mean
        line_fit = np.polyfit(clusters, mean_val, 4, w=weight)
        x = np.linspace(0, num_sats, 100)
        plt.plot(x, np.polyval(line_fit, x), lw=7, c="black", label="Mean Trend")

        if file_types[element] in ["eccentricity"]:
            std = np.std(flatten(data))
            mean = np.mean(flatten(data))
            plt.ylim([mean-(3*std), mean+(3*std)])
            # plt.yscale("log")
        
        plt.legend(fontsize=legend_size,)
        plt.savefig(image_location+"/"+file_types[element]+".png")
        plt.clf()
