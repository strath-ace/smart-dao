from commons import *

import numpy as np
import matplotlib.pyplot as plt
import math

classes = ["10", "20"]
thresholds = ["0", "05", "075"]
thresholds_i = [0, 0.5, 0.75]
ratios = ["01", "03", "05", "07", "09"]
ratios_i = [0.1, 0.3, 0.5, 0.7, 0.9]

f1_weighted = np.zeros((len(classes),len(thresholds),len(ratios)))
f1_weighted[f1_weighted == 0] = np.nan
f1_weighted_nb = np.zeros((len(classes),len(thresholds),len(ratios)))
f1_weighted_nb[f1_weighted_nb == 0] = np.nan
for i, clas in enumerate(classes):
    for j, threshold in enumerate(thresholds):
        for k, ratio in enumerate(ratios):
            try:
                results = load_json("results/model_stats_classes_"+clas+"_threshold_"+threshold+"_ratio_"+ratio+".json")
                f1_weighted[i,j,k] = results["f1-weighted"]
                f1_weighted_nb[i,j,k] = results["f1-weighted-no-background"]
            except:
                pass

color_scheme = "viridis"

fig, axs = plt.subplots(1,2,figsize=(15,5.5), layout="constrained")
axs = axs.flatten()

# fig.subplots_adjust(bottom=0.2)

axs[0].set_title("F1 Score for 10 Classes")
axs[0].imshow(
    f1_weighted[0], 
    vmin=np.nanmin(f1_weighted), 
    vmax=np.nanmax(f1_weighted), 
    cmap=color_scheme
)
axs[0].invert_yaxis()
axs[0].set_xticks(range(len(ratios)), ratios_i)
axs[0].set_xlabel("Loss Ratios")
axs[0].set_yticks(range(len(thresholds_i)), thresholds_i)
axs[0].set_ylabel("Thresholds")
for (j,i),label in np.ndenumerate(f1_weighted[0]):
    axs[0].text(i,j,round(label,3),ha='center',va='center')

axs[1].set_title("F1 Score for 20 Classes")
legend_data = axs[1].imshow(
    f1_weighted[1], 
    vmin=np.nanmin(f1_weighted), 
    vmax=np.nanmax(f1_weighted), 
    cmap=color_scheme
)
axs[1].invert_yaxis()
axs[1].set_xticks(range(len(ratios)), ratios_i)
axs[1].set_xlabel("Loss Ratios")
axs[1].set_yticks(range(len(thresholds_i)), thresholds_i)
axs[1].set_ylabel("Thresholds")
for (j,i),label in np.ndenumerate(f1_weighted[1]):
    axs[1].text(i,j,round(label,3),ha='center',va='center')

cbar = plt.colorbar(legend_data)
cbar.ax.set_ylabel("F1 Score")
plt.savefig("f1_scores.png")

plt.clf()



print(np.shape(f1_weighted))
print(np.shape(f1_weighted_nb))

# f1_weighted = np.around(f1_weighted, 3)
# f1_weighted_nb = np.around(f1_weighted_nb, 3)

def dec3(x):
    y = np.zeros(np.shape(x))
    y = np.array(y, dtype=str)
    for i in range(np.shape(x)[0]):
        for j in range(np.shape(x)[1]):
            for k in range(np.shape(x)[2]):
                # print(x[i,j,k])
                if not np.isnan(x[i,j,k]):
                    if round(x[i,j,k],3) == round(np.nanmax(x[i]),3):
                        y[i,j,k] = '\\textbf{'+f"{x[i,j,k]:.3f}"+'}'
                    else:
                        y[i,j,k] = f"{x[i,j,k]:.3f}"
                else:
                    y[i,j,k] = "nan"
    return y

f1_weighted = dec3(f1_weighted)
f1_weighted_nb = dec3(f1_weighted_nb)

print()
print("###############")
print("10 Crop Classes")
print()
# [classes, thresholds, ratios]
clas = 0
for i in range(np.shape(f1_weighted)[2]):
    line = str(ratios_i[i])+" & "
    line += f1_weighted[clas,0,i]+" & "+f1_weighted_nb[clas,0,i]+" & "
    line += f1_weighted[clas,1,i]+" & "+f1_weighted_nb[clas,1,i]+" & "
    line += f1_weighted[clas,2,i]+" & "+f1_weighted_nb[clas,2,i]+" \\\\"
    print(line)

print()
print("###############")
print("20 Crop Classes")
print()
clas = 1
for i in range(np.shape(f1_weighted)[2]):
    line = str(ratios_i[i])+" & "
    line += f1_weighted[clas,0,i]+" & "+f1_weighted_nb[clas,0,i]+" & "
    line += f1_weighted[clas,1,i]+" & "+f1_weighted_nb[clas,1,i]+" & "
    line += f1_weighted[clas,2,i]+" & "+f1_weighted_nb[clas,2,i]+" \\\\"
    print(line)

print()
print("###############")
print()