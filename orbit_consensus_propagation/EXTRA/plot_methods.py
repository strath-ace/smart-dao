# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import numpy as np
import matplotlib.pyplot as plt
import os
from commons import *
from os import listdir
from os.path import isfile, join



fig, ax1 = plt.subplots(figsize=(6,4))

###################### MOO ######################

###################### X COORDS ######################

x = []
for i in range(4, 100):
    x.append(i)

###################### BEAM ######################

beam = [6996240, 15612714, 10204733]

plt.plot(x[:len(beam)], beam, label="Beam")

###################### MOO ######################

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", "data_icsmd_100day")
opt_location = os.path.join(save_location, "moo2")
opt_data = os.path.join(opt_location, "data")

onlyfiles = [f for f in listdir(opt_data) if isfile(join(opt_data, f))]

files_open = []
for i in range(len(onlyfiles)):
    if onlyfiles[i][-5] == "f":
        files_open.append(onlyfiles[i])

all_times = []
max_iter = []
maxes = []
for OPEN in files_open:
    obj = np.load(opt_data+"/"+OPEN)

    history = []
    for i in obj.files:
        history.append(np.array((obj[i])))

    obj.close()

    F = history[-1]

    F = np.unique(F, axis=0)

    F = F[F[:,0] != 1]

    F[:,0] = F[:,0]
    F[:,1] = -F[:,1]

    min_times = []
    num_sats = []
    F_li = []
    for F in history:
        F2 = F[F[:,0] != 1]
        F2[:,1] = -F2[:,1]
        min_times = []
        num_sats = []
        if len(F2) != 0:
            for i in range(int(np.amin(F2[:,1])), int(np.amax(F2[:,1]))+1):
                min_times.append(np.amin(F2[F2[:,1] == i][:,0]))
                num_sats.append(i)
        F_li.append(min_times)

    max_length = 0
    for i in range(len(F_li)):
        if max_length < len(F_li[i]):
            max_length = len(F_li[i])

    for i in range(len(F_li)):
        while len(F_li[i]) < max_length:
            F_li[i].append(0)

    F_li = np.array(F_li)

    temp = []
    for i in range(len(F_li[0])):
        _, indx = np.unique(np.asanyarray(F_li[:,i], dtype=float), axis=0, return_index=True)
        temp.append(np.amax(indx))

    maxes.append(temp)

    max_length = 0
    for i in range(len(maxes)):
        if max_length < len(maxes[i]):
            max_length = len(maxes[i])

    for i in range(len(maxes)):
        while len(maxes[i]) < max_length:
            maxes[i].append(np.nan)

moo = np.nanmean(maxes, axis=0)

plt.plot(x[:len(moo)], moo*400, label="MOO")

###################### BRUTE FORCE ######################

brute = []
for i in range(4, 4+len(moo)):
    summer = 1
    n = 82
    r = i
    for j in range(n, n-r, -1):
        summer *= j
    for j in range(2,r):
        summer /= j
    brute.append(summer)

plt.plot(x[:len(moo)], brute, label="Brute")

###################### OUTPUT ######################

plt.ylim([1, 10*np.amax(brute)])
plt.yscale("log")

plt.title("")
plt.legend()


save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "PERM_DATA")
if not os.path.exists(save_location):
    os.makedirs(save_location)
plt.savefig(save_location+"/methods_plot.png")

plt.clf()

