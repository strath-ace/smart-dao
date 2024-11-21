import os
import numpy as np
import datetime
import matplotlib.pyplot as plt
from tqdm import tqdm
import itertools 
import matplotlib.animation as animation

from skyfield.api import load, EarthSatellite
from skyfield.iokit import parse_tle_file
from skyfield.elementslib import osculating_elements_of
from sgp4.api import Satrec, WGS72

import ctypes
from array import array

from common import *
from ga_fitness import fitness

open_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(open_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
if not os.path.exists(save_location):
    os.makedirs(save_location)

start_adder = 0

os.system("go build -buildmode=c-shared -o ./go_fit.so .")

ts = load.timescale()

satellites_no_sim = get_icsmd_satellites(open_location+"/active.tle", "icsmd_sats.txt")

start_date = datetime.datetime(2024,9,11, tzinfo=utc)

epoch = (start_date - datetime.datetime(1949,12,31,0,0, tzinfo=utc))
val = {
    "argp_i": -121.5016422844484,
    "ecc_i": 0.11409471636166019,
    "inc_i": -80.54973897064212,
    "raan_i": -33.83873369746696,
    "anom_i": 26.316195554368036,
    "mot_i": 6098.99280756073
}

argp_i = val["argp_i"]
ecc_i = val["ecc_i"]
inc_i = val["inc_i"]
raan_i = val["raan_i"]
anom_i = val["anom_i"]
mot_i = val["mot_i"]
# print(val)
satellite2 = Satrec()
satellite2.sgp4init(
    WGS72,                      # gravity model
    'i',                        # 'a' = old AFSPC mode, 'i' = improved mode
    25544,                      # satnum: Satellite number
    epoch.days,                 # epoch: days since 1949 December 31 00:00 UT
    3.8792e-05,                 # bstar: drag coefficient (1/earth radii)
    0.0,                        # ndot: ballistic coefficient (radians/minute^2)
    0.0,                        # nddot: mean motion 2nd derivative (radians/minute^3)
    ecc_i,                      # ecco: eccentricity
    np.deg2rad(argp_i),         # argpo: argument of perigee (radians)
    np.deg2rad(inc_i),          # inclo: inclination (radians)
    np.deg2rad(anom_i),         # mo: mean anomaly (radians)
    np.deg2rad(mot_i)/(24*60),  # no_kozai: mean motion (radians/minute)
    np.deg2rad(raan_i),         # nodeo: R.A. of ascending node (radians)
)
sim_sat = EarthSatellite.from_satrec(satellite2, ts)

satellites_with_sim = [sim_sat, *satellites_no_sim]




global global_frame_data
global_frame_data = []

animation_data = load_json("animation_data.json")

def update(frame):

    print("Frame number:", frame)

    completed_no_sim = np.array(animation_data[frame]["completed_no_sim"])
    completed_with_sim = np.array(animation_data[frame]["completed_with_sim"])
    position_no_sim = np.cbrt(np.array(animation_data[frame]["position_no_sim"]))
    position_with_sim = np.cbrt(np.array(animation_data[frame]["position_with_sim"]))
    

    if int(frame) == 0:
        global plot_data
        plot_data = []
        global plot_data2
        plot_data2 = []
        global time_data
        time_data = []

    time_data.append(animation_data[frame]["time_minutes"])


    ######## Fig 1

    ax[0].clear()

    colorer = np.full(len(satellites_no_sim), "red       ")
    if len(completed_no_sim) > 0:
        colorer[np.array(completed_no_sim)] = "green"
    colorer = np.char.strip(colorer)


    ax[0].set_xlim([-30, 30])
    ax[0].set_ylim([-30, 30])
    ax[0].set_zlim([-30, 30])
    # ax[1].set_xscale("log")
    # ax[1].set_yscale("log")
    # ax[1].set_zscale("log")
    ax[0].axis('off')
    ax[0].scatter(position_no_sim[:,0],position_no_sim[:,1],position_no_sim[:,2], color=colorer, s=10)
    ax[0].scatter([0],[0],[0], c="blue", s=6371, alpha=0.2)
    ax[0].set_title("Without simulated satellite")

    ######## Fig 2

    ax[1].clear()

    colorer2 = np.full(len(satellites_with_sim), "red       ")
    if len(completed_with_sim) > 0:
        colorer2[np.array(completed_with_sim)] = "green"
    colorer2[0] = "blue"
    colorer2 = np.char.strip(colorer2)

    ax[1].set_xlim([-30, 30])
    ax[1].set_ylim([-30, 30])
    ax[1].set_zlim([-30, 30])
    # ax[1].set_xscale("log")
    # ax[1].set_yscale("log")
    # ax[1].set_zscale("log")
    ax[1].axis('off')
    ax[1].scatter(position_with_sim[:,0],position_with_sim[:,1],position_with_sim[:,2], color=colorer2, s=10)
    ax[1].scatter([0],[0],[0], c="blue", s=6371, alpha=0.2)
    ax[1].set_title("With new simulated satellite")

    ########## Fig 3

    if len(completed_no_sim) > 0:
        plot_data.append(len(completed_no_sim)/len(satellites_no_sim))
    else:
        plot_data.append(0)
    if len(completed_with_sim) > 0:
        adder = len(completed_with_sim)
        if 0 in completed_with_sim:
            adder -= 1
        plot_data2.append(adder/len(satellites_no_sim))
    else:
        plot_data2.append(0)
    
    ax[2].clear()
    ax[2].plot(time_data, plot_data, color="orange", label="Without simulated satellite")
    ax[2].plot(time_data, plot_data2, color="blue", label="With simulated satellite")
    ax[2].legend(loc="lower right")
    ax[2].set_xlim([0,24*60])
    ax[2].set_ylim([0,1])
    ax[2].set_xlabel("Time (Minutes)")
    ax[2].set_ylabel("Percentage")
    ax[2].set_title("Percentage of satellites completed consensus round")
    

    return 




fig = plt.figure(figsize=(10, 6.8),layout="constrained")
gs = fig.add_gridspec(2, 2, height_ratios=[3, 1])
ax1 = fig.add_subplot(gs[0, 0], projection='3d')
ax2 = fig.add_subplot(gs[0, 1], projection='3d')
# ax3 = fig.add_subplot(212)
ax3 = fig.add_subplot(gs[1, :])
plt.subplots_adjust(wspace=0, hspace=0)
ax = [ax1, ax2, ax3]





# ani = animation.FuncAnimation(fig=fig, func=update, frames=10, interval=60)
ani = animation.FuncAnimation(fig=fig, func=update, frames=len(animation_data), interval=60)



# plt.show()
ani.save("animation.gif",dpi=250)