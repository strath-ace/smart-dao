# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import numpy as np
import matplotlib.pyplot as plt
import os
from commons import *
from os import listdir
from os.path import isfile, join

########################## PARAMATERS #########################

SAVE_DIR = "data_icsmd_100day"

######################### BUILD/FIND DIRECTORIES FOR DATA #########################

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("DATA FILE DOES NOT EXIST")
opt_location = os.path.join(save_location, "moo2")
if not os.path.exists(opt_location):
    raise Exception("NO DATA EXISTS TO PLOT")
opt_data = os.path.join(opt_location, "data")
if not os.path.exists(opt_data):
    raise Exception("NO DATA EXISTS TO PLOT")
opt_res = os.path.join(opt_location, "results")
if not os.path.exists(opt_res):
    os.makedirs(opt_res)

onlyfiles = [f for f in listdir(opt_data) if isfile(join(opt_data, f))]

F = []


for OPEN in onlyfiles:
    try:
        obj = np.load(opt_data+"/"+OPEN)
        stuff = np.unique(obj["F"], axis=0)
        
        stuff[:,1] = -stuff[:,1]

        max_sat = np.amax(stuff[:,1])

        temp = []
        for i in range(4, 100):
            if np.sum(stuff[:,1] == i) == 1:
                temp.append(stuff[stuff[:,1] == i,0].tolist()[0])
            else:
                temp.append(np.nan)
        F.append(temp)
    except:
        pass


F = np.array(F)

for i in range(len(F[0])-1, 0, -1):
    if not np.isnan(F[:,i]).all():
        F = F[:,:i+1]
        break
    

fig, axs = plt.subplots(figsize=(10,10), tight_layout=True)

for x in F:
    plt.scatter(range(4,4+len(x)), x, c="blue", alpha=0.3)

mean = np.nanmean(F, axis=0)
# plt.plot(range(4,4+len(mean)), mean, label="Average", c="green")

std = np.nanstd(F, axis=0)
# plt.plot(range(4,4+len(std)), std, label="Standard Distribution"s)

min_vals = np.nanmin(F, axis=0)
plt.scatter(range(4,4+len(min_vals)), min_vals, label="Pareto Front", c="red")
plt.plot(range(4,4+len(min_vals)), min_vals, c="black", alpha=0.2)



plt.xlabel("Number of Satellites in Subset")
plt.ylabel("Consensus Time")
plt.legend()
plt.savefig(opt_res+"/merged_curve.png")


####################### PERFORMANCE INDICATORS

pf = []
x_vals = range(4,4+len(min_vals))
for i in range(len(min_vals)):
    pf.append([x_vals[i], min_vals[i]])
pf = np.array(pf)

F2 = []
for j in range(len(F)):
    temp = []
    for i in range(len(min_vals)):
        if min_vals[j] != np.nan:
            temp.append([x_vals[i], F[j,i]])
    F2.append(temp)
F2 = np.array(F2)



from pymoo.indicators.gd import GD
from pymoo.indicators.gd_plus import GDPlus
from pymoo.indicators.igd import IGD
from pymoo.indicators.igd_plus import IGDPlus
from pymoo.indicators.hv import HV

all_metrics = []
for i, x in enumerate(F2):
    print("----------------------------------")
    print("Iteration:", i)
    x2 = x[np.logical_not(np.isnan(x[:,1]))]
    metrics = [GD(pf)(x2), GDPlus(pf)(x2), IGD(pf)(x2), IGDPlus(pf)(x2), HV(pf=pf)(x2)]
    print("Generational Distance:", metrics[0])
    print("Generational Distance Plus:", metrics[1])
    print("Inverted Generational Distance:", metrics[2])
    print("Inverted Generational Distance Plus:", metrics[3])
    print("Hypervolume:", metrics[4])
    all_metrics.append(metrics)

all_metrics = np.array(all_metrics)
# print(all_metrics)

plt.clf()

titles = ["Generational Distance", "Generational Distance Plus", "Inverted Generational Distance", "Inverted Generational Distance Plus", "Hypervolume"]

fig, axs = plt.subplots(1, len(titles), figsize=(20,5), tight_layout=True)

for i in range(len(titles)):
    this_metric = all_metrics[:,i]
    axs[i].set_title(titles[i])
    counts, bins = np.histogram(this_metric)
    n, bins, patches = axs[i].hist(bins[:-1], bins, weights=counts, density=True)
    y = ((1 / (np.sqrt(2 * np.pi) * np.std(this_metric))) * np.exp(-0.5 * (1 / np.std(this_metric) * (bins - np.mean(this_metric)))**2))
    axs[i].plot(bins, y, "--", c="red")
    axs[i].set_xlim([np.mean(this_metric)-(2*np.std(this_metric)), np.mean(this_metric)+(2*np.std(this_metric))])

plt.savefig(opt_res+"/metrics.png")