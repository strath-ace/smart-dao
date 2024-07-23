import numpy as np
from pytictoc import TicToc
import os
from commons import *
import matplotlib.pyplot as plt

SAVE_DIR = "data_icsmd_1day"
# how_many = 100
# TIMESTEP = 30
# NUM_ITERATIONS = 400

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("Sat Data not setup, run get_active_tle.py first")
many_data = os.path.join(save_location, "many")
if not os.path.exists(many_data):
    os.makedirs(many_data)

# dataset = load_json(save_location+"/dataset.json")
# START_TIME = dataset["timestamp"]

names = np.load(save_location+"/sat_data.npy")[1:,0]
n = 5 # (5,6)
# names = np.append(names[:n], names[n+1:])
# print(names)
# print(len(names))
# start_set = np.array(np.linspace(START_TIME, START_TIME+how_many*NUM_ITERATIONS*TIMESTEP, how_many), dtype=int)
# START_TIME += how_many*NUM_ITERATIONS*TIMESTEP + NUM_ITERATIONS*TIMESTEP

# start_set = np.append(start_set, np.array(np.linspace(START_TIME, START_TIME+how_many*NUM_ITERATIONS*TIMESTEP, how_many), dtype=int))

# counter = 0
# big = np.zeros((len(start_set), 81,81),dtype=float)
# c = 0
# for start in start_set:
#     try:
#         T = np.load(many_data+"/binary_"+str(start)+".npy")
#     except:
#         T = np.load(many_data+"_2/binary_"+str(start)+".npy")
#     big[c] += np.sum(T,axis=2)
#     c += 1

# names = names[names!="CARTOSAT2IRSP7"]



big = np.load(save_location+"/binary.npy")

print(np.shape(big))

summer = np.sum(big, axis=(0,2))

indx = np.argsort(summer)
fig, axs = plt.subplots(figsize=(7,15), dpi=400)
fig.subplots_adjust(left=0.3)

# names = np.array(names, dtype=str)


names_30 = ["TERRASARX",
            "TANDEMX",
            "VRSS2",
            "CARTOSAT2A",
            "KANOPUSV6",
            "KANOPUSV5",
            "JILIN104",
            "JILIN106",
            "WORLDVIEW2WV2",
            "CBERS4",
            "GAOFEN1",
            "GEOEYE1",
            "WORLDVIEW3WV3",
            "DUBAISAT2",
            "SENTINEL1A",
            "RADARSAT2",
            "GAOFEN302",
            "RCM2",
            "PLEIADES1B",
            "SENTINEL2B",
            "PLEIADES1A",
            "RCM1",
            "SENTINEL2A",
            "GAOFEN303",
            "RESOURCESAT2A",
            "RCM3",
            "GAOFEN3",
            "NOAA18",
            "CBERS4A",
            "LANDSAT8"]


names = names[indx]
names = names.tolist()

for i in range(len(names)):
    if names[i] not in names_30:
        names_30.append(names[i])


names = names_30
print(names)
print(len(names))
for i in range(len(names)):
    names[i] += " - "+str(i+1)

print(names)
names = np.array(names)
plt.barh(np.arange(len(summer)), summer[indx])
plt.plot([0,np.amax(summer)], [82-30.5,82-30.5], c="red", label="Top 30")

plt.yticks(np.arange(len(summer)), np.flip(names))

print(np.sum(summer[:30]/np.sum(summer)))

plt.xscale("log")
plt.xlabel("Number of timesteps")
plt.ylabel("Satellite Name")
plt.legend(loc="lower right")
plt.title("Number of timesteps where interactions occur")
# plt.xlim([1, pow(10,5)])
plt.savefig(save_location+"/set_pick.png")
plt.savefig(save_location+"/set_pick.pdf")
# plt.show()