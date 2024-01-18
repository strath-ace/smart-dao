# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import numpy as np
import matplotlib.pyplot as plt
import os
from py_lib.generic import *

########################## PARAMATERS #########################

OPEN_FILE = "run_f_big.npz"

SAVE_DIR = "data_icsmd_100day"

######################### BUILD/FIND DIRECTORIES FOR DATA #########################

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("DATA FILE DOES NOT EXIST")
opt_location = os.path.join(save_location, "moo")
if not os.path.exists(opt_location):
    raise Exception("NO DATA EXISTS TO PLOT")
opt_data = os.path.join(opt_location, "data")
if not os.path.exists(opt_data):
    raise Exception("NO DATA EXISTS TO PLOT")
opt_results = os.path.join(opt_location, "results")
if not os.path.exists(opt_results):
    os.makedirs(opt_results)
opt_vals = os.path.join(opt_results, "opt_vals")
if not os.path.exists(opt_vals):
    os.makedirs(opt_vals)
    
MASSIVE = load_json(save_location+"/dataset.json")["max_time"]
MAX_TIME = MASSIVE / (60*60)

obj = np.load(opt_data+"/"+OPEN_FILE)

history = []
for i in obj.files:
    history.append(np.array((obj[i])))

obj.close()

F = history[-1]

idx = F[:,0] == -1

F[:,0] = F[:,0]
F[:,1] = F[:,1]

F2 = F[idx,1:]

idx_sort = np.argsort(F2[:,1])

F2 = F2[idx_sort]

_, idx_unique = np.unique(F2[:,1], return_index=True)

F2 = F2[idx_unique]

print(F2)

approx_ideal = (F2.min(axis=0))
approx_nadir = (F2.max(axis=0))

nF = (F2 - approx_ideal) / (approx_nadir - approx_ideal)

for x in np.linspace(0,1,11):

    weights = np.array([x, 1-x])

    from pymoo.mcdm.pseudo_weights import PseudoWeights
    i = PseudoWeights(weights).do(nF)

    from pymoo.decomposition.asf import ASF
    decomp = ASF()
    i2 = decomp.do(nF, 1/weights).argmin()

    fig, axs = plt.subplots(figsize=(7,7))

    plt.plot(-F2[:,1], F2[:,0]*MAX_TIME, c="black", alpha=0.2)
    plt.scatter(-F2[:,1], F2[:,0]*MAX_TIME, c="blue")
    plt.scatter(-F2[i,1]+0.1, F2[i,0]*MAX_TIME, c="red", marker="x", s=200, label="Psuedo Weight Method")
    plt.scatter(-F2[i2,1], F2[i2,0]*MAX_TIME, c="green", marker="x", s=200, label="Decomp Method")

    plt.xlabel("Number of satellites in subset")
    plt.ylabel("Consensus Time (Hours)")
    plt.title(str(round(x,1))+"x Consensus Time       "+str(round(1-round(x,1),1))+"x Number of Sats")
    plt.legend()

    plt.savefig(opt_vals+"/"+str(round(10*x))+".png")

    plt.clf()