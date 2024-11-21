import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import itertools 

from skyfield.api import load, EarthSatellite
from skyfield.iokit import parse_tle_file
from skyfield.elementslib import osculating_elements_of
from sgp4.api import Satrec, WGS72

from common import *

open_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(open_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
if not os.path.exists(save_location):
    os.makedirs(save_location)

start_adder = 0



ts = load.timescale()

with load.open(open_location+"/active.tle") as f:
    satellites = list(parse_tle_file(f, ts))

print('Loaded', len(satellites), 'satellites')

all_starts = []
all_params = []
for sat in satellites:
    barycentric = sat.at(ts.utc(2024, 9, 11+start_adder, 0, 0, 0))
    all_starts.append(np.append(barycentric.position.km, barycentric.velocity.km_per_s))
    orbit_elements = osculating_elements_of(barycentric)

    temp = []
    temp.append(orbit_elements.argument_of_periapsis.degrees)
    temp.append(orbit_elements.eccentricity)
    temp.append(orbit_elements.inclination.degrees)
    temp.append(orbit_elements.longitude_of_ascending_node.degrees)
    temp.append(orbit_elements.mean_anomaly.degrees)
    temp.append(orbit_elements.mean_motion_per_day.degrees)
    all_params.append(temp)

all_starts = np.array(all_starts)
all_params = np.array(all_params)


# print(np.shape())
all_params = all_params[(np.sum(np.isnan(all_starts),axis=1))==0]
all_starts = all_starts[(np.sum(np.isnan(all_starts),axis=1))==0]

# print(all_starts)
# print(all_params)

fig = plt.figure(figsize=(10,10), layout="constrained")
ax = fig.add_subplot(projection='3d')
ax.scatter(all_starts[:,0],all_starts[:,1],all_starts[:,2])
ax.set_xlim([-50000, 50000])
ax.set_ylim([-50000, 50000])
ax.set_zlim(-50000, 50000)
plt.savefig(save_location+"/orbit_map_of_all_sats.png")

fig = plt.figure()
# all_params_plot = (all_params-np.nanmean(all_params,axis=0))/(3*np.nanstd(all_params,axis=0))
all_all_params = all_params
all_params_plot = all_params/[360, np.amax(all_params[:,1]), 180, 360, 360, np.amax(all_params[:,5])]
plt.violinplot(all_params_plot, [0,1,2,3,4,5], showmeans=False, showextrema=False, showmedians=False)
# plt.ylim([-1,1])
plt.xticks([0,1,2,3,4,5], ["ARGP", "ECC", "INC", "RAAN", "MA", "MM"])
plt.savefig(save_location+"/orbital_elements_of_all_sats.png")










satellites = get_satellites(open_location+"/active.tle", refine_by_name="icsmd_sats.txt")
# satellites = get_random_satellites(open_location+"/active.tle")


all_starts = []
all_params = []
for sat in satellites:
    barycentric = sat.at(ts.utc(2024, 9, 11+start_adder, 0, 0, 0))
    all_starts.append(np.append(barycentric.position.km, barycentric.velocity.km_per_s))
    orbit_elements = osculating_elements_of(barycentric)

    temp = []
    temp.append(orbit_elements.argument_of_periapsis.degrees)
    temp.append(orbit_elements.eccentricity)
    temp.append(orbit_elements.inclination.degrees)
    temp.append(orbit_elements.longitude_of_ascending_node.degrees)
    temp.append(orbit_elements.mean_anomaly.degrees)
    temp.append(orbit_elements.mean_motion_per_day.degrees)
    all_params.append(temp)

all_starts = np.array(all_starts)
all_params = np.array(all_params)


# print(np.shape())
all_params = all_params[(np.sum(np.isnan(all_starts),axis=1))==0]
all_starts = all_starts[(np.sum(np.isnan(all_starts),axis=1))==0]


fig = plt.figure(figsize=(10,10), layout="constrained")
ax = fig.add_subplot(projection='3d')
ax.scatter(all_starts[:,0],all_starts[:,1],all_starts[:,2])
ax.set_xlim([-50000, 50000])
ax.set_ylim([-50000, 50000])
ax.set_zlim(-50000, 50000)
plt.savefig(save_location+"/subgroup_orbit_map_of_all_sats.png")

fig = plt.figure()
# all_params_plot = (all_params-np.nanmean(all_params,axis=0))/(3*np.nanstd(all_params,axis=0))
# all_params_plot = all_params/np.amax(all_params,axis=0)
all_params_plot = all_params.copy()
all_params_plot[:,1] = np.log10(all_params_plot[:,1])
all_params_plot[:,1] = all_params_plot[:,1]+7
all_params_plot = all_params_plot/[360, 7, 180, 360, 360, np.amax(all_params[:,5])]

plt.violinplot(all_params_plot, [0,1,2,3,4,5], showmeans=False, showextrema=False, showmedians=False)

def deg2rad(x):
    return (x*7)-7

def rad2deg(x):
    return (x-7)/7

secax = plt.gca().secondary_yaxis('right', functions=(deg2rad, rad2deg))
secax.set_ylabel('Eccentricity Log10 Scale')

target_points = [0.5,0.5,0.5,0.5,0.5,0.5]
target_points_scaled = (target_points-np.nanmean(all_params,axis=0))/(3*np.nanstd(all_params,axis=0))
# plt.scatter([0,1,2,3,4,5], target_points_scaled, label="GA Optimised Orbital Elements")
# plt.ylim([-1,1])
plt.title("Standard Score of Orbital Parameters in ICSMD Subset")
plt.xticks([0,1,2,3,4,5], ["ARGP", "ECC", "INC", "RAAN", "MA", "MM"])
plt.legend()
plt.savefig(save_location+"/subgroup_orbital_elements_of_all_sats.png")
plt.clf()









data_all = []
for i in range(10):
    try:
        file_name = "data-ga/participants_4_startday_{:02d}_conntime_10.json".format(int(i))
        data = load_json(file_name)
        data = data[1:]
        data_all.append(data)
    except:
        break

points_to_scatter = []
for i in range(10):
    try:
        x = [xi["x"] for xi in data_all[i]]
        f = [xi["f"] for xi in data_all[i]]
    except:
        continue
    
    best_coords_pos = np.argmin(f[-1])
    # print(best_coords_pos)
    X = x[-1][best_coords_pos]

    points_to_scatter.append([X["argp_i"], (X["ecc_i"]), X["inc_i"], X["raan_i"], X["anom_i"], X["mot_i"]/(360)])

points_to_scatter = np.array(points_to_scatter)

fig, axs = plt.subplots(1,6, figsize=(20,10), layout="tight")


all_params[all_params[:,0] > 180,0] = all_params[all_params[:,0] > 180,0] -360
all_all_params[all_all_params[:,0] > 180,0] = all_all_params[all_all_params[:,0] > 180,0] -360

all_params[:,1] = (all_params[:,1]) # Log Eccentricity
all_all_params[:,1] = (all_all_params[:,1]) # Log Eccentricity

all_params[all_params[:,2] > 90,2] = all_params[all_params[:,2] > 90,2] - 180
all_all_params[all_all_params[:,2] > 90,2] = all_all_params[all_all_params[:,2] > 90,2] - 180

all_params[all_params[:,3] > 180,3] = all_params[all_params[:,3] > 180,3] -360
all_all_params[all_all_params[:,3] > 180,3] = all_all_params[all_all_params[:,3] > 180,3] -360

all_params[all_params[:,4] > 180,4] = all_params[all_params[:,4] > 180,4] -360
all_all_params[all_all_params[:,4] > 180,4] = all_all_params[all_all_params[:,4] > 180,4] -360

all_params[:,5] = (all_params[:,5])/360 # Log Eccentricity
all_all_params[:,5] = (all_all_params[:,5])/360 # Log Eccentricity

colors = plt.cm.hsv(np.linspace(0, 1, len(points_to_scatter)))

for i in range(6):
    parts_all = axs[i].violinplot(all_all_params[:,i], [0], widths=1, showmeans=False, showextrema=False, showmedians=False)
    parts_icsmd =  axs[i].violinplot(all_params[:,i], [0], widths=0.5, showmeans=False, showextrema=False, showmedians=False)
    axs[i].scatter([0]*len(points_to_scatter), points_to_scatter[:,i], c=colors, marker="x", label="Orbital Elements to Improve Consensus")
    for pc in parts_all['bodies']:
        pc.set_facecolor('#1E3231')
        pc.set_alpha(0.2)
    for pc in parts_icsmd['bodies']:
        pc.set_facecolor('#1E3231')
        pc.set_alpha(0.5)
    axs[i].set_title(["Argument of Periapsis (Degrees)", "Eccentricity (0-1)", "Inclination (Degrees)", "RAAN (Degrees)", "Mean Anomoly (Degrees)", "Mean Motion (Revolutions/Day)"][i])
    axs[i].get_xaxis().set_visible(False)
    axs[i].set_ylim([ [-180, 180],[0,0.15],[-90,90],[-180,180],[-180,180],[0,6500/360]][i])

center_on = 0
axs[center_on].scatter([0],[-1000], color='#1E3231', label="All Satellites", alpha=0.2)
axs[center_on].scatter([0],[-1000], color='#1E3231', label="ICSMD Subset Satellites", alpha=0.5)
leg = axs[center_on].legend(ncol=3, fontsize="20")
bb = leg.get_bbox_to_anchor().transformed(axs[center_on].transAxes.inverted())
# bb.x0 += -0.3
# bb.x1 += -0.3
bb.y0 += -0.1
bb.y1 += -0.1
leg.set_bbox_to_anchor(bb, transform = axs[center_on].transAxes)

plt.savefig(save_location+"/subgroup_orbital_elements_of_all_sats_split.png")
plt.clf()