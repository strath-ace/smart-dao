# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import matplotlib.pyplot as plt

labels = [
    "Copernicus Activation",
    "ICSMD Activation",
    "100s of Tweets with Keywords",
    "Media about event",
    "USGS 'Did you feel it' Notifications",
    "Tsunami Warnings from GTS"
]
    
colours = [
    "orange",
    "blue",
    "darkviolet",
    "crimson",
    "green",
    "peru"
]

alphas = [1, 1, 0.5, 0.5, 0.5, 0.5]


fig = plt.figure(figsize=(7, 5), dpi=500)
for i in range(len(labels)):
    plt.plot([1, 0], [0, 0], linewidth=5, label=labels[i], color=colours[i], alpha=alphas[i])
plt.xlim([0, 100])
plt.legend(loc='upper center')
plt.savefig("legend")



