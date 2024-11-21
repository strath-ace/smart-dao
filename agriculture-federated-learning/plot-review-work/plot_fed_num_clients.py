from commons import *

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import random
import itertools
from matplotlib.gridspec import GridSpec

PARAM_partition_style = ["iid"]
PARAM_num_classes = [11]
PARAM_num_clients = [2, 4, 8, 16, 32, 64, 128, 256]


SQUARE_AXIS = False

all_results = load_json("all_results.json")

# print(all_results)
combo = list(itertools.product(PARAM_partition_style, PARAM_num_classes, PARAM_num_clients))
# print(list(combos))
# print(combo)

res_per_combo = []
f1_per_combo = []
for i, comb in enumerate(combo):
    starter_builder = []
    starter_builder_f1 = []
    for starter in range(10):
        for ii in range(len(all_results)):
            temp = []
            b1 = starter == all_results[ii]["starter"]
            b2 = comb[0] == all_results[ii]["partition_style"]
            b3 = comb[1] == all_results[ii]["num_classes"]
            b4 = comb[2] == all_results[ii]["num_clients"]
            if b1 and b2 and b3 and b4:
                temp.append(all_results[ii]["results"]["f1_weighted"])  
                temp.append(all_results[ii]["results"]["f1_weighted_no_background"])
                temp.append(all_results[ii]["results"]["f1_macro"])

                precision = np.array(all_results[ii]["results"]["precision"])
                recall = np.array(all_results[ii]["results"]["recall"])
                true_counts = np.array(all_results[ii]["results"]["true_counts"])
                temp.append((np.sum(precision*true_counts,axis=1)/np.sum(true_counts,axis=1)))
                temp.append((np.sum(recall*true_counts,axis=1)/np.sum(true_counts,axis=1)))

                temp.append(all_results[ii]["results"]["loss"])
                # temp.append(np.array(all_results[ii]["results"]["f1"])[:,0].tolist())
                f1_scores = (all_results[ii]["results"]["f1"])

                starter_builder.append(temp)
                starter_builder_f1.append(f1_scores)
    res_per_combo.append(starter_builder)
    f1_per_combo.append(starter_builder_f1)


cmap = plt.cm.jet
norm = mpl.colors.LogNorm(vmin=1, vmax=np.amax(np.array(PARAM_num_clients,dtype=int)))
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)

fig,axs = plt.subplots(1,3, figsize=(15,8), layout="constrained")

print("#############")
print("Results")
print()
for x, y in zip(combo, res_per_combo):
    if len(np.shape(y)) == 3:
        # Take max value in each iteration and then mean over all iterations
        # print(np.shape(y))
        averaged = np.mean(np.amax(np.array(y), axis=2), axis=0)
        # averaged = np.mean(np.array(y),axis=0)
        # last_values = [averaged[3,-1], averaged[4,-1], averaged[0,-1], averaged[1,-1], averaged[2,-1]]
        last_values = [averaged[3], averaged[4], averaged[0], averaged[1], averaged[2]]
        last_values = np.array(np.around(last_values,3), dtype=str)
        # print(x[2], "\t", x[1], "\t", x[0], "\t", " & ".join(last_values) )
        print(x[2], "&", x[1]-1, "& \\text{True} &", " & ".join(last_values), "\\\\" )    
print()
print("#############")
print()

# Plot F1-Weighted

cc = 0
maximum = 0
for x, y in zip(combo, res_per_combo):
    if len(np.shape(y)) == 3:
        print(np.shape(y))
        averaged = np.mean(y,axis=0)
        std = np.std(np.array(y),axis=0)
        if SQUARE_AXIS:
            averaged = np.square(averaged)
            std = np.square(std)
        axs[0].plot(averaged[0], c=cmap(norm(int(x[2]))))
        axs[0].fill_between(np.arange(len(averaged[0])), averaged[0]-std[0], averaged[0]+std[0], color=cmap(norm(int(x[2]))), alpha=0.2)
        maximum = np.amax([maximum, *averaged[0]+std[0]]) 
        cc += 1
if SQUARE_AXIS:
    tickers = np.ceil(np.sqrt(np.linspace(0,maximum,7))*100)/100
    axs[0].set_yticks(np.square(tickers), (tickers))


# Plot F1-Weighted No background
# cutter = [0,1,3,4]
cc = 0
maximum = 0
for x, y in zip(combo, res_per_combo):
    if len(np.shape(y)) == 3:
        # averaged = np.mean(np.array(y)[cutter],axis=0)
        # std = np.std(np.array(y)[cutter],axis=0)
        averaged = np.mean(np.array(y),axis=0)
        std = np.std(np.array(y),axis=0)
        if SQUARE_AXIS:
            averaged = np.square(averaged)
            std = np.square(std)
        labels = str(x[2])+" clients"
        axs[1].plot(averaged[1], label=labels, c=cmap(norm(int(x[2]))))
        axs[1].fill_between(np.arange(len(averaged[1])), averaged[1]-std[1], averaged[1]+std[1], color=cmap(norm(int(x[2]))), alpha=0.2)
        maximum = np.amax([maximum, *averaged[1]+std[1]]) 
        cc += 1
if SQUARE_AXIS:
    tickers = np.ceil(np.sqrt(np.linspace(0,maximum,7))*100)/100
    axs[1].set_yticks(np.square(tickers), (tickers))

# Plot Loss

cc = 0
maximum = 0
minimum = 1
target = 5
for x, y in zip(combo, res_per_combo):
    if len(np.shape(y)) == 3:
        averaged = np.mean(np.array(y),axis=0)
        std = np.std(np.array(y),axis=0)
        if SQUARE_AXIS:
            averaged = np.sqrt(averaged)
            std = np.sqrt(std)
        labels = str(x[2])+" clients"
        axs[2].plot(averaged[target], c=cmap(norm(int(x[2]))))
        axs[2].fill_between(np.arange(len(averaged[target])), averaged[target]-std[target], averaged[target]+std[target], color=cmap(norm(int(x[2]))), alpha=0.1)
        maximum = np.amax([maximum, *averaged[target]+std[target]])
        minimum = np.amin([minimum, *averaged[target]+std[target]]) 
        cc += 1
if SQUARE_AXIS:
    tickers = np.ceil(np.square(np.linspace(minimum,maximum,7))*100)/100
    axs[2].set_yticks(np.sqrt(tickers), (tickers))


axs[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4, frameon=False)
# plt.subplots_adjust(bottom=0.6)
# axs[0].set_ylim([-0.02,1])
axs[0].set_xticks([0,5,10,15,20])
axs[0].set_xlabel("Aggregation Rounds")
axs[0].set_ylabel("F1-Score Weighted")
axs[0].set_title("Client Number Comparison - F1-Score Weighted")
# axs[1].set_ylim([-0.02,1])
axs[1].set_xticks([0,5,10,15,20])
axs[1].set_xlabel("Aggregation Rounds")
axs[1].set_ylabel("F1-Score Weighted (No Background)")
axs[1].set_title("Client Number Comparison - F1-Score Weighted (No Background)")
# axs[2].set_ylim([0.8,1])
axs[2].set_xticks([0,5,10,15,20])
axs[2].set_xlabel("Aggregation Rounds")
axs[2].set_ylabel("F1-Score Weighted (No Background)")
axs[2].set_title("Client Number Comparison - Centralised Testset Loss")
plt.savefig("client_number_comparison.png")
plt.clf()








# fig,axs = plt.subplots(2,4, figsize=(20, 10), layout="constrained")
# axs = axs.flatten()

colourful = False

fig = plt.figure(figsize=(20, 10))

gs = GridSpec(3, 4, width_ratios=[1,1, 1, 1], height_ratios=[1,0.2,1])
# Plot F1-Weighted
cc = 0
ccc = 0
# cutter = [0,1,3,4]
for x, y, z in zip(combo, f1_per_combo, res_per_combo):
    if len(np.shape(y)) == 3 and len(np.shape(z)) == 3:
        started = False
        if cc == 4:
            cc = 0
            ccc = 2
        if colourful:
            color1 = cmap(norm(int(x[2])))
            color2 = cmap(norm(int(x[2])))
        else:
            color1 = "black"
            color2 = "red"
        axs = fig.add_subplot(gs[ccc, cc])  
        # if int(x[2]) == 2:
        #     averaged = np.mean(np.array(y)[cutter],axis=0)
        #     averaged_f = np.mean(np.array(z)[cutter],axis=0)
        # else:
        averaged = np.mean(np.array(y),axis=0)
        averaged_f = np.mean(np.array(z),axis=0)
        for yi in range(np.shape(averaged)[1]):
            if yi == 0:
                line1 = axs.plot(averaged[:,yi], "--", label="Background Class", c=color1, alpha=0.4)[0]
            else:
                if not started:
                    line2 = axs.plot(averaged[:,yi], label="Individual Classes", c=color1, alpha=0.4)[0]
                    started = True
                else:
                    axs.plot(averaged[:,yi], c=color1, alpha=0.4)
        line3 = axs.plot(averaged_f[1], label="Weighted F1 (No Background)", c=color2)[0]
        axs.set_title(str(x[2])+" Clients", fontsize=18)
        axs.set_xticks([0,5,10,15,20])
        axs.set_ylim([-0.02,1])
        axs.set_xlabel("Aggregation Rounds")
        axs.set_ylabel("F1-Score")
        leg1 = axs.legend(handles=[line1, line2], loc='upper center', bbox_to_anchor=(0.5, -0.13), ncol=2, frameon=False)
        leg2 = axs.legend(handles=[line3], loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=1, frameon=False)
        axs.add_artist(leg1)
        axs.add_artist(leg2)
        cc += 1

fig.subplots_adjust(left=0.04, right=0.96)
fig.suptitle("Per Class F1-Score for Different Numbers of Clients", fontsize=30)

plt.savefig("client_number_comparison_per_class.png")
plt.clf()