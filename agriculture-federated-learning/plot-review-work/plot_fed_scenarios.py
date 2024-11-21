from commons import *

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import random
import itertools
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D

PARAM_partition_style = ["iid", "niid"]
PARAM_num_classes = [11, 21]
PARAM_num_clients = [2, 32]


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
    for starter in range(25):
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
                temp.append(np.array(all_results[ii]["results"]["f1"])[:,0].tolist())
                f1_scores = (all_results[ii]["results"]["f1"])

                starter_builder.append(temp)
                starter_builder_f1.append(f1_scores)
    res_per_combo.append(starter_builder)
    f1_per_combo.append(starter_builder_f1)


hexadecimal_alphabets = '0123456789ABCDEF'
get_color = ["#" + ''.join([random.choice(hexadecimal_alphabets) for j in
range(6)]) for i in range(len(combo))]

plt.figure(figsize=(8,10), layout="constrained")

print("#############")
print("Results")
print()
for x, y in zip(combo, res_per_combo):
    # Take max value in each iteration and then mean over all iterations
    averaged = np.mean(np.amax(np.array(y), axis=2), axis=0)
    # averaged = np.mean(np.array(y),axis=0)
    # last_values = [averaged[3,-1], averaged[4,-1], averaged[0,-1], averaged[1,-1], averaged[2,-1]]
    last_values = [averaged[3], averaged[4], averaged[0], averaged[1], averaged[2]]
    last_values = np.array(np.around(last_values,3), dtype=str)
    if x[0] == "iid":
        print(x[2], "&", x[1]-1, "& \\text{True} &", " & ".join(last_values), "\\\\" )  
    else:
        print(x[2], "&", x[1]-1, "& \\text{False} &", " & ".join(last_values), "\\\\" )  
    # print(x[2], "\t", x[1], "\t", x[0], "\t", " & ".join(last_values) )
print()
print("#############")
print()

fig,axs = plt.subplots(1,3, figsize=(15,8), layout="constrained")

# Plot F1-Weighted

cc = 0
for x, y in zip(combo, res_per_combo):
    averaged = np.mean(y,axis=0)
    std = np.std(np.array(y),axis=0)
    axs[0].plot(averaged[0], c=get_color[cc])
    axs[0].fill_between(np.arange(len(averaged[0])), averaged[0]-std[0], averaged[0]+std[0], color=get_color[cc], alpha=0.2)
    cc += 1

# Plot F1-Weighted No background

cc = 0
for x, y in zip(combo, res_per_combo):
    averaged = np.mean(y,axis=0)
    std = np.std(np.array(y),axis=0)
    labels = [" ".join(np.array(x,dtype=str))]
    axs[1].plot(averaged[1], label=labels, c=get_color[cc])
    axs[1].fill_between(np.arange(len(averaged[1])), averaged[1]-std[1], averaged[1]+std[1], color=get_color[cc], alpha=0.2)
    cc += 1

# Plot Loss

cc = 0
target = 5
for x, y in zip(combo, res_per_combo):
    if len(np.shape(y)) == 3:
        averaged = np.mean(np.array(y),axis=0)
        std = np.std(np.array(y),axis=0)
        axs[2].plot(averaged[target], c=get_color[cc])
        axs[2].fill_between(np.arange(len(averaged[target])), averaged[target]-std[target], averaged[target]+std[target], color=get_color[cc], alpha=0.2)
        cc += 1



axs[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4, frameon=False)
# axs[0].subplots_adjust(bottom=0.6)
# axs[0].set_ylim([-0.02,1])
axs[0].set_xticks([0,5,10,15,20])
axs[0].set_xlabel("Aggregation Rounds")
axs[0].set_ylabel("F1-Score Weighted")
axs[0].set_title("All scenarios comparison - F1-Score Weighted")
# axs[1].set_ylim([-0.02,1])
axs[1].set_xticks([0,5,10,15,20])
axs[1].set_xlabel("Aggregation Rounds")
axs[1].set_ylabel("F1-Score Weighted (No Background)")
axs[1].set_title("All Scenarios Comparison - F1-Score Weighted (No Background)")
# axs[2].set_ylim([0,1])
axs[2].set_xticks([0,5,10,15,20])
axs[2].set_xlabel("Aggregation Rounds")
axs[2].set_ylabel("F1-Score Weighted (No Background)")
axs[2].set_title("All Scenarios Comparison - Centralised Testset Loss")
plt.savefig("all_comparisons.png")
plt.clf()









##### CLASS IMBALANCE VIEWER


id_list = np.array([255, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64])

name_list = np.array(["Background", "pasture", "maize", "winter wheat", "potatoes", "fodder beets", "leguminous cover",    "winter barley", "pears", "appels", "beans", "engelwortel", "hemp", "cauliflower", "fodder carrots",    "other crops", "brussels sprouts", "triticale", "sjalots", "leek", "chicory", "peas", "fodder mixture", "spinach",    "parsnip", "strawberries", "cherry", "spring barley", "vegetables - seeds", "cucumber herb", "zucchini",    "winter rapeseed", "asparagus", "spring wheat", "fodder cabbages", "butternut", "sword herd", "haricot",    "winter rye", "grape seedlings", "ornamental plants", "other annual fruit", "buckwheat", "fodder turnips",    "tagetes", "blueberries", "fennel", "red berries", "raspberry", "other fodder crops", "aromatic herbs", "sorghum",    "soybeans", "yellow mustard", "tobacco", "walnuts", "barley", "spring rapeseed", "kiwi berries", "spring rye",    "plums", "chervil", "phacelia", "gooseberries", "hazelnuts", "sunflower"])

count_list = np.array([
    208288074, 68096739, 50068391, 16664081, 14379282, 6565216, 4502781, 3933897, 2582060, 1488258, 1417765, 
    1255222, 1067147, 1043146, 1009874, 1001480, 912454, 831751, 827927, 780744, 748404, 705120, 625563, 528456, 
    301429, 291863, 289896, 244321, 243480, 216599, 181351, 157622, 146538, 132405, 128322, 113114, 88687, 
    87384, 85854, 59326, 56964, 53807, 45499, 42663, 37126, 27031, 26752, 21415, 17584, 15525, 13340, 13042, 
    12271, 11877, 11793, 9260, 8821, 7944, 7369, 6328, 6090, 5653, 4977, 2909, 1564, 1013
])

counter = []
counter_name = []
id_list[id_list > 20] = 0
counter.append(int(np.sum(count_list[id_list == 0])))
counter_name.append(str(name_list[0]))
for i in range(len(id_list)):
    if id_list[i] != 0:
        counter.append(int(count_list[i]))
        counter_name.append(str(name_list[i]))

# class_10 = (all_results[0]["results"]["true_counts"][0])
class_20_test = np.array(all_results[-1]["results"]["true_counts"][0])
class_20_train = np.array(counter)


plt.clf()
plt.figure(figsize=(20,7), layout="constrained")
plt.bar(range(len(class_20_train)), height=class_20_train, label="Federated Training Dataset", alpha=0.5)
plt.bar(range(len(class_20_test)), height=class_20_test, label="Centralised Test Dataset", alpha=0.5)
plt.legend(fontsize=18)
plt.yscale("log")
plt.xlabel("Crop Class", fontsize=18)
plt.xticks(range(len(class_20_train)), counter_name, rotation=-90, fontsize=18)
plt.ylabel("Pixel Count", fontsize=18)
plt.title("Crop Class Imbalance Showcase", fontsize=20)
plt.subplots_adjust(bottom=0.3)
plt.savefig("class_imbalance_showcase.png")
plt.clf()










# fig,axs = plt.subplots(2,4, figsize=(15,8), layout="constrained")
# axs = axs.flatten()

fig = plt.figure(figsize=(20, 10))

gs = GridSpec(2, 5, width_ratios=[1,1, 0.3, 1, 1])

# Plot F1-Weighted
cc = 0
# cutter = [0,1,2,4]
started = []
for x, y, z in zip(combo, f1_per_combo, res_per_combo):
    print(np.shape(np.array(y)))
    if len(np.shape(y)) == 3 and len(np.shape(z)) == 3:
        # if int(x[2]) == 2:
        #     averaged = np.mean(np.array(y)[cutter],axis=0)
        #     averaged_f = np.mean(np.array(z)[cutter],axis=0)
        # else:
        averaged = np.mean(np.array(y),axis=0)
        averaged_f = np.mean(np.array(z),axis=0)

        if x[1] == 11:
            i = 0
        else:
            i = 1
        if x[2] == 2:
            j = 0
        else:
            j = 1
        if x[0] == "iid":
            k = 0
        else:
            k = 1
        axs = fig.add_subplot(gs[k,j+(i*2)+i])
        for yi in range(np.shape(averaged)[1]):
            if yi == 0:
                # axs.plot(averaged[:,yi], "--", c=get_color[cc], alpha=0.3)
                line1 = axs.plot(averaged[:,yi], "--", label="Background Class", c="black", alpha=0.3)[0]
            else:
                # axs.plot(averaged[:,yi], c=get_color[cc], alpha=0.3)
                if not started:
                    line2 = axs.plot(averaged[:,yi], label="Individual Classes", c="black", alpha=0.3)[0]
                    started = True
                else:
                    axs.plot(averaged[:,yi], c="black", alpha=0.3)
        # axs.plot(averaged_f[1], c=get_color[cc])
        line3 = axs.plot(averaged_f[1], c="red", label="Weighted F1 (No Background)")[0]
    axs.set_xticks([0,5,10,15,20])
    axs.set_ylim([-0.02,1])
    axs.set_xlabel("Aggregation Rounds")
    axs.set_ylabel("F1-Score")
    if j == 0 and k == 1:
        axs.text(10, -0.3, "2 Clients", ha="center", fontsize=18)
    if j == 1 and k == 1:
        axs.text(10, -0.3, "32 Clients", ha="center", fontsize=18)
    if j == 0 and k == 0:
        axs.text(-8, 0.5, "IID", va="center", fontsize=18, rotation=90)
    if j == 0 and k == 1:
        axs.text(-8, 0.5, "Non-IID", va="center", fontsize=18, rotation=90)
    cc += 1

# Line on the left side of the plot area
left_line_1 = Line2D([0.035, 0.035], [0.05, 0.9], color="black", linewidth=2, transform=fig.transFigure)
left_line_2 = Line2D([0.52, 0.52], [0.05, 0.9], color="black", linewidth=2, transform=fig.transFigure)
bottom_line_1 = Line2D([0.035, 0.47], [0.05, 0.05], color="black", linewidth=2, transform=fig.transFigure)
bottom_line_2 = Line2D([0.52, 0.955], [0.05, 0.05], color="black", linewidth=2, transform=fig.transFigure)
fig.add_artist(left_line_1)
fig.add_artist(left_line_2)
fig.add_artist(bottom_line_1)
fig.add_artist(bottom_line_2)

axs.legend(handles=[line1, line2, line3], loc='upper center', bbox_to_anchor=(-1.52, 2.35), ncol=3, frameon=False, fontsize=10)
# axs.add_artist(leg1)

fig.text(0.2525, 0.9, "10 Classes", ha="center", fontsize=22)

fig.text(0.7375, 0.9, "20 Classes", ha="center", fontsize=22)

fig.subplots_adjust(left=0.07, right=0.93)
fig.suptitle("Per Class F1-Score for Different Federated Learning Scenarios", fontsize=30)

plt.savefig("scenario_comparison_per_class.png")
plt.clf()







