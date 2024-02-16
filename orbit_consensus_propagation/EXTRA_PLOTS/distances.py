import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.interpolate import make_interp_spline

SAVE_DIR = "data_icsmd_1day"

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("Sat Data not setup, run get_active_tle.py first")

for_view = np.load(save_location+"/all_distances.npy")
si = np.shape(for_view)

fig = plt.figure(figsize = (20, 15))
# ax = plt.axes(projection ="3d")

for y in for_view[2]:
    if np.mean(y) < 0.5*1E9:
        window_size = 100
        i = 0
        moving_averages = []
        while i < len(y) - window_size + 1:
            window_average = round(np.sum(y[i:i+window_size]) / window_size, 2)
            moving_averages.append(window_average)
            i += 1
 
        plt.plot(moving_averages)


# x_li = np.array(np.linspace(0,si[0]-1, si[0]), dtype=int)
# y_li = np.array(np.linspace(0,si[1]-1, si[1]), dtype=int)

# plt.yscale("log")
# ax.scatter3D(x, y, z)
plt.savefig(save_location+"/distances.png")