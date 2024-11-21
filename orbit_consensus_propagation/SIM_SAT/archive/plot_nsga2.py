import numpy as np
import matplotlib.pyplot as plt

from common import *

data = load_json("data-ga/pop50_gen50_nsga2.json")

# data = data[1:]

f = np.array([xi["non-dominated-solutions"] for xi in data])
print(f)

print(np.shape(f))


plt.scatter(f[-1,:,0], f[-1,:,1])
# plt.xlim([,0])
plt.ylim([0, 24*60*2])
plt.savefig("figures/ga/non-dominated-solution.png")
plt.clf()

# argp = [[xii["argp_i"] for xii in xi] for xi in x]
# ecc = [[xii["ecc_i"] for xii in xi] for xi in x]
# inc = [[xii["inc_i"] for xii in xi] for xi in x]
# raan = [[xii["raan_i"] for xii in xi] for xi in x]
# anom = [[xii["anom_i"] for xii in xi] for xi in x]
# mot = [[xii["mot_i"] for xii in xi] for xi in x]






# colors = plt.cm.viridis_r(np.linspace(0, 1, len(argp)))

# fig = plt.figure(figsize=(10,12), layout="tight")
# gs = plt.GridSpec(3, 3, height_ratios=[1, 1, 1])

# ax1 = fig.add_subplot(gs[0, 0])
# ax1.set_title("Argument of Periapsis")
# for i in range(len(argp)):
#     ax1.scatter(argp[i], f[i], color=colors[i])

# ax2 = fig.add_subplot(gs[0, 1])
# ax2.set_title("Eccentricity")
# for i in range(len(ecc)):
#     ax2.scatter(ecc[i], f[i], color=colors[i])

# ax3 = fig.add_subplot(gs[0, 2])
# ax3.set_title("Inclination")
# for i in range(len(inc)):
#     ax3.scatter(inc[i], f[i], color=colors[i])

# ax4 = fig.add_subplot(gs[1, 0])
# ax4.set_title("RAAN")
# for i in range(len(raan)):
#     ax4.scatter(raan[i], f[i], color=colors[i])

# ax5 = fig.add_subplot(gs[1, 1])
# ax5.set_title("Mean Anomoly")
# for i in range(len(anom)):
#     ax5.scatter(anom[i], f[i], color=colors[i])

# ax6 = fig.add_subplot(gs[1, 2])
# ax6.set_title("Mean Motion")
# for i in range(len(mot)):
#     ax6.scatter(mot[i], f[i], color=colors[i])

# ax7 = fig.add_subplot(gs[2, :])
# ax7.set_title("Fitness over generations")
# ax7.set_xlabel("Generation")
# ax7.set_ylabel("Fitness")
# for i in range(len(f)):
#     ax7.scatter([i]*len(f[i]), f[i], color=colors[i])

# plt.savefig("figures/ga/learning_orbit_elements.png")
# plt.clf()