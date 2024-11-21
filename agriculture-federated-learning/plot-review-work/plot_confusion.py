from commons import *

import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.gridspec import GridSpec

classes = ["10", "20"]
thresholds = ["0", "05", "075"]
thresholds_i = [0, 0.5, 0.75]
ratios = ["01", "03", "05", "07", "09"]
ratios_i = [0.1, 0.3, 0.5, 0.7, 0.9]


fig = plt.figure(figsize=(40, 12))
# Define a 3x2 GridSpec but with extra height spacing after the first row
gs = GridSpec(3, 11, width_ratios=[1,1,1, 1, 1, 0.3, 1,1, 1, 1,1])

# fig, axs = plt.subplots(3,6,figsize=(20,10), layout="constrained")
# axs = axs.flatten()
# axs = [axs[[0,1,2]],axs[[6,7,8]],axs[[12,13,14]]], [axs[[3,4,5]],axs[[9,10,11]],axs[[15,16,17]]]
color_scheme = "viridis"
# confusion_data = np.zeros((len(classes),len(thresholds),len(ratios)))
# confusion_data[confusion_data == 0] = np.nan
axes = []
for i, clas in enumerate(classes):
    for j, threshold in enumerate(thresholds):
        for k, ratio in enumerate(ratios):
            try:
            # print("data/confusion_classes_"+clas+"_threshold_"+threshold+"_ratio_"+ratio+".npy")
                results = np.load("results/confusion_classes_"+clas+"_threshold_"+threshold+"_ratio_"+ratio+".npy")
            except:
                pass
            axs = fig.add_subplot(gs[j,k+(i*5)+i])
            legend_res = axs.imshow(results, vmin=0, vmax=1, cmap=color_scheme)
            # axs[i][j][k].set_xlabel("Prediction")
            # axs[i][j][k].set_ylabel("Truth")
            axs.invert_yaxis()
            if clas == "10":
                tickers = [0,5,10]
            elif clas == "20":
                tickers = [0,5,10,15,20]
            # axs[i][j][k].set_xticks(tickers)
            # axs[i][j][k].set_yticks(tickers)
            axs.set_xticks([])
            axs.set_yticks([])
            # axs[i][j][k].axis("off")
            axes.append(axs)

fig.subplots_adjust(left=0.02, right=0.98, top=1, bottom=0, wspace=0.2, hspace=0.1)
# axs[0][2][0].set_xlabel("0.1")
# axs[0][2][1].set_xlabel("0.3")
# axs[0][2][2].set_xlabel("0.5")
# axs[1][2][0].set_xlabel("0.1")
# axs[1][2][1].set_xlabel("0.3")
# axs[1][2][2].set_xlabel("0.5")
# axs[0][0][0].set_ylabel("0.75")
# axs[0][1][0].set_ylabel("0.5")
# axs[0][2][0].set_ylabel("0")

            # axs[i][j][k].set_title("Ratio = "+ratio+" | Threshold = "+threshold)

# print(confusion_data)
# plt.colorbar(legend_res)
cbar = fig.colorbar(legend_res, ax=axes, fraction=0.05, pad=0.02, shrink=0.85)





plt.savefig("confusion.png")

plt.clf()





