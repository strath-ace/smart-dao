import matplotlib.pyplot as plt
import numpy as np
from pytictoc import TicToc
import os
from itertools import combinations_with_replacement
from numpy import arange as ran
import sys
from commons import *
from matrix_sparsify import sparse_to_dense
np.set_printoptions(edgeitems=15)

ticcer = TicToc()



SAVE_DIR = "data_icsmd_1day"
how_many = 100
TIMESTEP = 30
NUM_ITERATIONS = 400
max_time = NUM_ITERATIONS

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("Sat data not setup")
save_location1 = save_location
dataset = load_json(save_location+"/dataset.json")
START_TIME = dataset["timestamp"]

sat_attributes = np.load(save_location+"/sat_data.npy")[1:]
headings = np.load(save_location+"/sat_data.npy")[0]

all_sat_attributes = np.load(save_location+"/sat_data_all_sats.npy")[1:]

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    raise Exception("No data in data")
many_out = os.path.join(save_location, "many_out")
if not os.path.exists(many_out):
    raise Exception("No data in many out")


start_set = np.array(np.linspace(START_TIME, START_TIME+how_many*NUM_ITERATIONS*TIMESTEP, how_many), dtype=int)
START_TIME += how_many*NUM_ITERATIONS*TIMESTEP + NUM_ITERATIONS*TIMESTEP
start_set = np.append(start_set, np.array(np.linspace(START_TIME, START_TIME+how_many*NUM_ITERATIONS*TIMESTEP, how_many), dtype=int))
used_sats_20 = np.array([5, 13, 50,  8, 12, 25,  9, 36, 34, 29, 47, 30, 38, 23,  7, 17, 45, 71, 69, 75])
used_sats_30 = np.array([5, 13, 50,  8, 67, 66, 52, 54, 12, 36, 25,  9, 34, 29, 30,  7, 79, 71, 23, 47, 17, 69, 38, 80, 45, 70, 42,  2, 75, 24])
outer_counter = np.arange(len(used_sats_30))

dataset20 = []
for start in start_set:
    try:
        x = np.load(many_out+"/x_"+str(start)+".npy")
        x2 = np.load(many_out+"/x2_"+str(start)+".npy")

        used_sats = used_sats_20

        # print("################")

        phases = []
        for p in range(4):
            sats = []
            for i in range(np.shape(x)[1]):
                sat = np.arange(max_time)[np.array(x[p,i,:max_time],dtype=bool)]
                if len(sat) == 1:
                    sats.append(sat[0])
                else:
                    sats.append(np.nan)
            phases.append(sats)
        phases = np.array(phases)
        phases = phases.swapaxes(0,1)

        consensus_time = np.nanmax(phases)
        # print("Consensus Time", consensus_time)
        
        primary = used_sats[phases[:,0] == 0][0]
        # print("Primary", primary)

        conn_sats = used_sats[~np.isnan(phases[:,2])]
        # print("Conn Sats", conn_sats)

        dataset20.append([round(start-np.amin(start_set),-3), consensus_time, primary, conn_sats])
    except:
        pass
# print(dataset)
dataset20 = np.array(dataset20, dtype=object)

dataset30 = []
big_T = np.empty((81,81,0))
for start in start_set:
    try:
        x = np.load(many_out+"/x_other_"+str(start)+".npy")
        x2 = np.load(many_out+"/x2_other_"+str(start)+".npy")

        used_sats = used_sats_30

        

        # print("################")

        phases = []
        for p in range(4):
            sats = []
            for i in range(np.shape(x)[1]):
                sat = np.arange(max_time)[np.array(x[p,i,:max_time],dtype=bool)]
                if len(sat) == 1:
                    sats.append(sat[0])
                else:
                    sats.append(np.nan)
            phases.append(sats)
        phases = np.array(phases)
        phases = phases.swapaxes(0,1)

        consensus_time = np.nanmax(phases)
        # print("Consensus Time", consensus_time)
        
        primary = used_sats[phases[:,0] == 0][0]
        # print("Primary", primary)

        conn_sats = used_sats[~np.isnan(phases[:,2])]
        # print("Conn Sats", conn_sats)

        dataset30.append([round(start-np.amin(start_set),-3), consensus_time, primary, conn_sats])

        try:
            T = np.load(save_location1+"/many_2/binary_"+str(start)+".npy")
        except:
            T = np.load(save_location1+"/many/binary_"+str(start)+".npy")
        big_T = np.append(big_T, T, axis=2) 

    except:
        pass

# print(dataset)
dataset30 = np.array(dataset30, dtype=object)





all_conn_sats20 = np.array(list(dataset20[:,3]),dtype=int).flatten()

unique_sats20, unique_sats_count20 = np.unique(all_conn_sats20, return_counts=True)

all_conn_sats = np.array(list(dataset30[:,3]),dtype=int).flatten()

unique_sats, unique_sats_count = np.unique(all_conn_sats, return_counts=True)

unique_sats_count_bigger_20 = []
for i in range(len(unique_sats)):
    if unique_sats[i] in unique_sats20:
        for j in range(len(unique_sats20)):
            if unique_sats[i] == unique_sats20[j]:
                unique_sats_count_bigger_20.append(unique_sats_count20[j])
    else:
        unique_sats_count_bigger_20.append(0)
unique_sats_count20 = np.array(unique_sats_count_bigger_20)





indx = np.flip(np.argsort(unique_sats_count))
unique_sats = unique_sats[indx]
unique_sats_count = unique_sats_count[indx]
sat_counter = np.arange(len(unique_sats_count))
# outer_counter = outer_counter[indx]


unique_sats20 = unique_sats[indx]
unique_sats_count20 = unique_sats_count20[indx]


sat_attributes_new = sat_attributes[unique_sats]



s = np.round(np.array(sat_attributes_new[:,1:], dtype=float), 5)
# Just icmsd
s2 = np.round(np.array(sat_attributes[:,1:], dtype=float), 5)
# All all satellites
s2 = np.round(np.array(all_sat_attributes[:,1:], dtype=float), 5)

headings_labels = [*headings]




div1 = s[unique_sats_count == np.amax(unique_sats_count),:]
# div2 = s[unique_sats_count > np.mean(unique_sats_count[~(unique_sats_count == np.amax(unique_sats_count))])]
# div3 = s[unique_sats_count <= np.mean(unique_sats_count[~(unique_sats_count == np.amax(unique_sats_count))])]
div25 = s[:round(len(s)/5)]
div50 = s[:round(len(s)/2)]
div100 = s[round(len(s)/2):]
# div15 = s[unique_sats_count > np.median(unique_sats_count[unique_sats_count > np.median(unique_sats_count)])]
div2 = s[unique_sats_count > np.median(unique_sats_count)]
div3 = s[unique_sats_count <= np.median(unique_sats_count)]

titles = ["Mean Motion", "Inclination", "Right Ascension of the Ascending Node", "Eccentricity", "Argument of Periapsis", "Mean anomaly"] 

for i in [0,1,2,3,4,5]:
    plt.figure(figsize=(10,6),dpi=200)
    bigger = len(s[:,i])
    wid = [1, math.sqrt(len(div100[:,i])/bigger), math.sqrt(len(div50[:,i])/bigger), math.sqrt(len(div25[:,i])/bigger)]
    # violin = plt.violinplot([s2[:,i], s[:,i], div3[:,i], div2[:,i], div15[:,i], div1[:,i]], [0,1,2,3,4,5], points=100, widths=wid, showmeans=True, showextrema=True, showmedians=False)
    violin = plt.violinplot([s[:,i], div100[:,i], div50[:,i], div25[:,i]], [0,1,2,3], points=100, widths=wid, showmeans=False, showextrema=False, showmedians=False)
    # plt.xlabel(headings_labels[x_val+1])#
    plt.xticks([0,1,2,3], ["Major Subset (n)", "Lower 50% of Satellites", "Upper 50% of Satellites", "Top 20% of Satellites"], rotation=-10)
    ## Explanation
    ## Lower half is the lower half of occuranes in m. How often the score is
    plt.ylabel(headings_labels[i+1])

    if i == 0:
        plt.title("")
        plt.ylim([14,15.5])
    elif i == 1:
        plt.ylim([97.25,99])
    elif i == 3:
        plt.yscale("log")

    plt.title(titles[i])
    plt.savefig(save_location+"/"+headings[i+1]+".png")
    plt.savefig(save_location+"/eps/"+headings[i+1]+".pdf")
    plt.clf()


###################### Plot occurances of primary and all ########################

plt.figure(figsize=(11,10),dpi=200)

# Count all occurances
all_sats = np.array([])
for i in range(len(dataset30[:,3])):
    all_sats = np.append(all_sats, dataset30[:,3][i])
all_uniq, all_uniq_c = np.unique(all_sats, return_counts=True)
all_uniq_c = 100*all_uniq_c/(len(dataset30[:,3]))
all_indx = np.flip(np.argsort(all_uniq_c))
all_uniq = all_uniq[all_indx]


outro_counter = np.zeros(len(all_uniq), dtype=int)
for i in range(len(all_uniq)):
    outro_counter[i] = outer_counter[(used_sats_30 == int(all_uniq[i]))][0]

all_uniq_c = all_uniq_c[all_indx]
plt.stairs(all_uniq_c, np.arange(len(all_uniq_c)+1)-0.5, fill=True, label="Occurances in Subset")

# Count primaries
prim_uniq_c = []
for i in all_uniq:
    prim_uniq_c.append(np.sum(dataset30[:,2] == i))
prim_uniq_c = np.array(prim_uniq_c)
prim_uniq_c = 100*prim_uniq_c/(len(dataset30[:,2]))
plt.stairs(prim_uniq_c, np.arange(len(prim_uniq_c)+1)-0.5, fill=True, label="Occurances as Primary")

plt.plot([len(div1)-0.5,len(div1)-0.5], [0,np.amax(all_uniq_c)], c="red", linewidth="2", label="Top/20%/50%")
plt.plot([len(div25)-0.5,len(div25)-0.5], [0,np.amax(all_uniq_c)], c="red", linewidth="2")
plt.plot([len(div50)-0.5,len(div50)-0.5], [0,np.amax(all_uniq_c)], c="red", linewidth="2")


plt.xticks(np.arange(len(all_uniq_c)), outro_counter+1)#np.array(all_uniq,dtype=int))
plt.xlabel("Satellite that is in consensus")
plt.ylabel("Percentage of time each sat is in consensus")
plt.title("How often each satellite in consensus")
plt.legend()
plt.savefig(save_location+"/all_occurances.png")
plt.savefig(save_location+"/eps/all_occurances.pdf")
plt.clf()

########################### Rest vs rest ##############################

plt.figure(figsize=(11,10),dpi=200)

all_sat_conn = []
for i in range(len(unique_sats)):
    this_sat_conn = []
    for j in range(len(dataset30)):
        if unique_sats[i] in dataset30[j,3]:
            this_sat_conn.append(dataset30[j,3])
    all_sat_conn.append(np.array(this_sat_conn))
# all_sat_conn = np.array(all_sat_conn)
# print(all_sat_conn)

count_arr = np.zeros((len(all_sat_conn), len(unique_sats)))
for i in range(len(all_sat_conn)):
    # print(all_sat_conn[i])s
    for k in range(len(unique_sats)):
        for j in range(len(all_sat_conn[i])):
            if unique_sats[k] in all_sat_conn[i][j]:
                count_arr[i,k] += 1
    count_arr[i] = count_arr[i] / len(all_sat_conn[i])
 
count_arr = count_arr.swapaxes(0,1) * 100
count_arr = np.round(count_arr, 2)

plt.imshow(count_arr)
plt.gca().invert_yaxis()
plt.xticks(np.arange(len(unique_sats)), outro_counter+1)
plt.yticks(np.arange(len(unique_sats)), outro_counter+1)
# Plot red lines to divide into most common, more common, less common
plt.plot([len(div1)-0.5,len(div1)-0.5], [-0.5,np.shape(count_arr)[0]-0.5], c="red", linewidth="2")
plt.plot([len(div25)-0.5,len(div25)-0.5], [-0.5,np.shape(count_arr)[0]-0.5], c="red", linewidth="2")
plt.plot([len(div50)-0.5,len(div50)-0.5], [-0.5,np.shape(count_arr)[0]-0.5], c="red", linewidth="2")
plt.xlabel("In subset")
plt.ylabel("Also in subset")
plt.title("Percentage chance that 2 satellites are in same subset")
plt.colorbar(label="Percentage chance both satellites in subset")
plt.savefig(save_location+"/any_vs_any.png")
plt.savefig(save_location+"/eps/any_vs_any.pdf")
plt.clf()

########################### Primary vs rest ##############################

plt.figure(figsize=(11,10),dpi=200)

all_sat_conn = []
for i in range(len(unique_sats)):
    this_sat_conn = []
    for j in range(len(dataset30)):
        if unique_sats[i] == dataset30[j,2]:
            this_sat_conn.append(dataset30[j,3])
    all_sat_conn.append(np.array(this_sat_conn))

count_arr = np.zeros((len(all_sat_conn), len(unique_sats)))
for i in range(len(all_sat_conn)):
    # print(all_sat_conn[i])s
    for k in range(len(unique_sats)):
        for j in range(len(all_sat_conn[i])):
            if unique_sats[k] in all_sat_conn[i][j]:
                count_arr[i,k] += 1
    count_arr[i] = count_arr[i] / len(all_sat_conn[i])
    
count_arr = count_arr.swapaxes(0,1) * 100
count_arr = np.round(count_arr, 2)

plt.imshow(count_arr)
plt.gca().invert_yaxis()
plt.xticks(np.arange(len(unique_sats)), outro_counter+1)
plt.yticks(np.arange(len(unique_sats)), outro_counter+1)
plt.xlabel("Primary node")
plt.ylabel("Other nodes in subset")
plt.title("Percentage chance that satellite is in subset due to primary")
plt.colorbar(label="Percentage chance that satellite is in subset due to primary")
plt.savefig(save_location+"/primary_vs_any.png")
plt.savefig(save_location+"/eps/primary_vs_any.pdf")
plt.clf()



########################## Picked out conections #############################

big_T = big_T[used_sats_30][:,used_sats_30]

fig, axs = plt.subplots(5,6, figsize=(24,20),sharex=True, sharey=True, dpi=400)
print(np.shape(big_T))
j = 0
k = 0
for i in np.arange(30):
    
    axs[k,j].imshow(np.swapaxes(big_T[i,:,:], 0,1), aspect='auto', interpolation='none')
    sat_name = sat_attributes_new[i,0]

    axs[k,j].set_title("Sat "+str(outro_counter[i]+1)+" - "+sat_name)

    j += 1
    if j >= 6:
        j = 0
        k += 1

plt.xticks(np.arange(len(unique_sats)),[" "]*len(unique_sats))
fig.supxlabel("Interactions with other satellites", fontsize=30)
fig.supylabel("Timesteps", fontsize=30)
fig.suptitle("Satellite interactions", fontsize=40)
# plt.tight_layout()
plt.gca().invert_yaxis()
plt.savefig(save_location+"/satellite_interactions_all.png")
plt.savefig(save_location+"/eps/satellite_interactions_all.pdf")
plt.clf()