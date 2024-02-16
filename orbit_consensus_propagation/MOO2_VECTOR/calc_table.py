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

MAX_TIME = 100  # Days

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




mean = np.nanmean(F, axis=0)

std = np.nanstd(F, axis=0)

min_vals = np.nanmin(F, axis=0)

sat_num = range(4, 4+len(min_vals))

print(F)

sums = np.sum(np.logical_not(np.isnan(F)), axis=0)

print("Satellite number | Pareto Front | Mean | Std | Found items")
for i in range(len(min_vals)):
    print(sat_num[i], min_vals[i], mean[i], std[i], sums[i])

# print(mean, std, min_vals)

import pandas as pd

fig, ax = plt.subplots(figsize=(10,7))

# hide axes
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')

# df = pd.DataFrame( columns=list(["Satellite number", "Pareto Front", "Mean", "Std", "Number of solutions"]))

print(np.round(min_vals / sat_num, 3))


the_table = ax.table(cellText=np.rot90(np.rot90(np.rot90([np.round(sums), np.round(100*std,5), np.round(100*mean,5), np.round(100*min_vals,5), np.round(sat_num)]))), colLabels=["Satellite number", "Pareto Front", "Mean", "Std", "Number of solutions"], loc='center')
the_table.auto_set_font_size(False)
the_table.auto_set_column_width(col=list(range(5)))
fig.tight_layout()

plt.savefig(opt_res+"/table.png")