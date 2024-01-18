import matplotlib.pyplot as plt
import csv
from py_lib.generic import *
import os
import numpy as np

import numpy as np                 # v 1.19.2
import pandas as pd                # v 1.1.3
import matplotlib.pyplot as plt    # v 3.3.2
import seaborn as sns              # v 0.11.0

# Create sample dataset
# rng = np.random.default_rng(seed=123)  # random number generator
# df = pd.DataFrame(dict(variable = rng.normal(size=1000)))

file_names = ["data_all", "data_icsmd"]
name_names = ["All", "ICSMD"]
special = [0, -1]

dis_li = ["10 km", "50 km","100 km","500 km","1000 km"]

for j in range(len(file_names)):

    save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_names[j])
    if not os.path.exists(save_location):
        os.makedirs(save_location)

    title = name_names[j]+" satellites unique combinations histogram"
    title2 = name_names[j]+" satellites unique combinations line plot"

    km_li = np.asarray(csv_input(save_location+"/all_combs.csv"), dtype="float64")
    km_li = np.rot90(km_li)

    # for i in range(len(km_li)):
    #     km_li[i] = np.sort(km_li[i])

    for i in range(len(km_li)-1, special[j], -1):
        this_step = km_li[i]

        if j == 0:
            num_bins = round(np.amax(km_li[-1])/200)
        elif j == 1:
            num_bins = round(np.amax(km_li[i])/2)

        # Plot seaborn histogram overlaid with KDE
        ax = sns.histplot(data=this_step, bins=num_bins, stat='density', alpha= 0.5, kde=True,
                        edgecolor='white', linewidth=0,
                        line_kws=dict(color='black', alpha=1, linewidth=2, label=dis_li[i]))
        ax.legend(frameon=False)

    # plt.axis("equal")
    plt.legend()
    plt.xlim([0,len(this_step)])
    # plt.yscale("log")
    # plt.ylim([0, 0.007])
    # plt.xscale("log")
    plt.xlabel("Number of in range satellites")
    plt.ylabel("Number of satellites (%)")
    plt.title(title)
    plt.savefig(save_location+"/histogram_unique.png")
    # plt.show()

    plt.clf()

    for i in range(len(km_li)-1, -1, -1):
        this_step = km_li[i]
        plt.plot(np.sort(this_step), label=dis_li[i])
    plt.xlabel("Satellites (Ordered by number in range)")
    plt.ylabel("Number of in range satellites")
    plt.legend()
    plt.title(title2)
    plt.savefig(save_location+"/lineplot_unique.png")
    plt.clf()

    print("Done",file_names[j])