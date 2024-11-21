import numpy as np
import matplotlib.pyplot as plt

from common import *

data = load_json("data-ga/0_completed.json")

num_sim_sats = 2

data = data[1:]

x = [xi["x"] for xi in data]
f = [xi["f"] for xi in data]

all_var = []
for i in range(num_sim_sats):
    argp = [[xii["argp_i_"+str(i)] for xii in xi] for xi in x]
    ecc = [[xii["ecc_i_"+str(i)] for xii in xi] for xi in x]
    inc = [[xii["inc_i_"+str(i)] for xii in xi] for xi in x]
    raan = [[xii["raan_i_"+str(i)] for xii in xi] for xi in x]
    anom = [[xii["anom_i_"+str(i)] for xii in xi] for xi in x]
    mot = [[xii["mot_i_"+str(i)] for xii in xi] for xi in x]
    all_var.append(argp)
    all_var.append(ecc)
    all_var.append(inc)
    all_var.append(raan)
    all_var.append(anom)
    all_var.append(mot)

# all_var = np.array(all_var)
print(np.shape(all_var))

# all_var = np.swapaxes(all_var, 0, 2)

colors = plt.cm.viridis_r(np.linspace(0, 1, len(argp)))

fig = plt.figure(figsize=(10,16), layout="tight")
gs = plt.GridSpec(6, 3, height_ratios=[1,1,1,1,1,1])
 
for j in range(num_sim_sats):
    ax1 = fig.add_subplot(gs[j*2, 0])
    ax1.set_title("Argument of Periapsis")
    for i in range(len(all_var[j*2+0])):
        ax1.scatter(all_var[j*2+0][i], f[i], color=colors[i])

    ax2 = fig.add_subplot(gs[j*2, 1])
    ax2.set_title("Eccentricity")
    for i in range(len(all_var[j*2+1])):
        ax2.scatter(all_var[j*2+1][i], f[i], color=colors[i])

    ax3 = fig.add_subplot(gs[j*2, 2])
    ax3.set_title("Inclination")
    for i in range(len(all_var[j*2+2])):
        ax3.scatter(all_var[j*2+2][i], f[i], color=colors[i])

    ax4 = fig.add_subplot(gs[j*2+1, 0])
    ax4.set_title("RAAN")
    for i in range(len(all_var[j*2+3])):
        ax4.scatter(all_var[j*2+3][i], f[i], color=colors[i])

    ax5 = fig.add_subplot(gs[j*2+1, 1])
    ax5.set_title("Mean Anomoly")
    for i in range(len(all_var[j*2+4])):
        ax5.scatter(all_var[j*2+4][i], f[i], color=colors[i])

    ax6 = fig.add_subplot(gs[j*2+1, 2])
    ax6.set_title("Mean Motion")
    for i in range(len(all_var[j*2+5])):
        ax6.scatter(all_var[j*2+5][i], f[i], color=colors[i])

ax7 = fig.add_subplot(gs[4:, :])
ax7.set_title("Fitness over generations")
ax7.set_xlabel("Generation")
ax7.set_ylabel("Fitness")
for i in range(len(f)):
    ax7.scatter([i]*len(f[i]), f[i], color=colors[i])

plt.savefig("figures/ga/learning_orbit_elements.png")
plt.clf()