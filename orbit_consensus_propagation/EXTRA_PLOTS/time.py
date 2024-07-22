import numpy as np
from pytictoc import TicToc
import os
from commons import *
import matplotlib.pyplot as plt

SAVE_DIR = "data_icsmd_1day"
how_many = 100
TIMESTEP = 30
NUM_ITERATIONS = 400

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("Sat Data not setup, run get_active_tle.py first")
many_data = os.path.join(save_location, "many")
if not os.path.exists(many_data):
    os.makedirs(many_data)

dataset = load_json(save_location+"/dataset.json")
START_TIME = dataset["timestamp"]

names = np.load(save_location+"/sat_data.npy")[1:,0]
# print(len(names))

start_set = np.array(np.linspace(START_TIME, START_TIME+how_many*NUM_ITERATIONS*TIMESTEP, how_many), dtype=int)
START_TIME += how_many*NUM_ITERATIONS*TIMESTEP + NUM_ITERATIONS*TIMESTEP

start_set = np.append(start_set, np.array(np.linspace(START_TIME, START_TIME+how_many*NUM_ITERATIONS*TIMESTEP, how_many), dtype=int))

counter = 0
big = np.zeros((len(start_set), 81,81),dtype=float)
c = 0
for start in start_set:
    try:
        T = np.load(many_data+"/binary_"+str(start)+".npy")
    except:
        T = np.load(many_data+"_2/binary_"+str(start)+".npy")
    big[c] += np.sum(T,axis=2)
    c += 1

print(np.shape(big))

summer = np.sum(big, axis=(0,2))



indx = np.argsort(summer)

names = names[indx]
for i in range(len(names)):
    names[len(names)-i-1] += " - "+str(i+1)

fig, axs = plt.subplots(figsize=(7,15), dpi=400)
fig.subplots_adjust(left=0.3)
plt.barh(np.arange(len(summer)), summer[indx])
plt.plot([0,pow(10,5)], [82-30.5,82-30.5], c="red", label="Top 30")

plt.yticks(np.arange(len(summer)), names)

plt.xscale("log")
plt.xlabel("Number of timesteps")
plt.ylabel("Satellite Name")
plt.legend(loc="lower right")
plt.title("Number of timesteps where interactions occur")
# plt.xlim([1, pow(10,5)])
plt.savefig(save_location+"/set_pick.png")
plt.savefig(save_location+"/set_pick.pdf")