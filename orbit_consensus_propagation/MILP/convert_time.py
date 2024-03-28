import numpy as np
from pytictoc import TicToc
import os
from commons import *

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

START_TIME += how_many*NUM_ITERATIONS*TIMESTEP + NUM_ITERATIONS*TIMESTEP
print(START_TIME)
start_set = np.array(np.linspace(START_TIME, START_TIME+how_many*NUM_ITERATIONS*TIMESTEP, how_many), dtype=int)
print(start_set-START_TIME)
counter = 0
for start in start_set:
    T = np.load(many_data+"/binary_"+str(start)+".npy")#[:,:,:400]

    ticcer = TicToc()
    ticcer2 = TicToc()

    print(np.shape(T))

    sh = np.shape(T)

    c = 0
    all_data = np.zeros((np.sum(np.arange(sh[2]+1)), sh[0], sh[0]), dtype=bool)
    ticcer.tic()
    for x in range(1,sh[2]+1):
        z = np.array(np.any(np.lib.stride_tricks.sliding_window_view(T,(sh[0],sh[0],x))[0,0], axis=3), dtype=bool)
        all_data[c:c+np.shape(z)[0],:,:] = z
        c += np.shape(z)[0]
        print(str(x)+"/"+str(sh[2]))
    ticcer.toc()
    # print("Saving to file")
    np.savez_compressed("data/many_converted/conv_"+str(start), t=all_data)
    print("Number", counter, "done")
    counter += 1
    # print("Done")
