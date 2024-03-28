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

start_set = np.array(np.linspace(START_TIME, START_TIME+how_many*NUM_ITERATIONS*TIMESTEP, how_many), dtype=int)

counter = 0
big = np.zeros((len(start_set), 81,81),dtype=float)
c = 0
for start in start_set:
    T = np.load(many_data+"/binary_"+str(start)+".npy")
    big[c] += np.sum(T,axis=2)
    c += 1

# spots = [1,6,9,14]#,54, 1,2,3,4,5,7,8,10,11,12,13]

summed = np.sum(big,axis=0)
big[big == 0] = np.nan
print(summed)
# indx = np.flip(np.argsort(np.sum(summed,axis=0)))
indx = np.flip(np.argsort(np.nanstd(summed,axis=0)))


summed = summed[indx][:,indx]
print("Best 20:", indx[:20])
print("Best 30:", indx[:30])
plt.imshow(np.log10(summed))
plt.show()

