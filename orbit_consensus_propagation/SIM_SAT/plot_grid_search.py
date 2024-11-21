import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
import itertools
import matplotlib.cm as cm
import matplotlib.colors as mcolors

from common import *

data_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(data_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
if not os.path.exists(save_location):
    os.mkdir(save_location)
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures", "orbital-elements")
if not os.path.exists(save_location):
    os.mkdir(save_location)

combinati = itertools.combinations(["argp","ecc","inc","raan","anom","mot"],2)

fig, axes = plt.subplots(4, 4, figsize=(17, 15),layout="constrained")
axes = axes.flatten()
c = 0

cmap = cm.inferno
norm = mcolors.Normalize(vmin=16, vmax=26)

for comb in tqdm(list(combinati)):

    try:
        data = np.load(data_location+"/contact_num_"+comb[0]+"_"+comb[1]+".npy")
        # data = np.load("contact_num.npy")
        json_data = load_json(data_location+"/details_"+comb[0]+"_"+comb[1]+".json")
    except:
        continue

    data = np.squeeze(data)
    print(np.amin(data), np.amax(data))
    while len(np.shape(data)) > 2:
        data = np.amax(data, axis=np.argmin(np.shape(data)))

    

    extent = [np.nanmin(json_data[comb[0]]), np.nanmax(json_data[comb[0]]),np.nanmax(json_data[comb[1]]),np.nanmin(json_data[comb[1]])]

    axes[c].imshow(np.swapaxes(data,0,1), extent=extent, aspect="auto", norm=norm, cmap=cmap)
    axes[c].set_xlabel(comb[0])
    axes[c].set_ylabel(comb[1])
    axes[c].invert_yaxis()

    c += 1


    # plt.figure(figsize=(10,10), layout="constrained")
    # plt.imshow(np.swapaxes(data,0,1), extent=extent, aspect="auto")
    # plt.xlabel(comb[0])
    # plt.ylabel(comb[1])
    # plt.colorbar()
    # plt.gca().invert_yaxis()
    # plt.savefig(save_location+"/"+comb[0]+"_"+comb[1]+".png")

axes[-1].axis("off")


sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([]) 
cbar = fig.colorbar(sm, ax=axes, orientation='vertical', fraction=0.2, pad=0.04)
cbar.set_label('Number of satellites completed a consensus round')

plt.savefig(save_location+"/all.png")