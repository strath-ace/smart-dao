import matplotlib.pyplot as plt
import numpy as np
import os
from commons import *

SAVE_DIR = "data_icsmd_1day"

# Create save location if not already exist
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("DATA FILE DOES NOT EXIST")

ga_data = csv_input(save_location+"/ga_results.csv")

num_genes = []
fitness = []

for x in ga_data:
    if float(x[1]) > -999999999999:
        num_genes.append(float(x[0]))
        fitness.append(-float(x[1]))

plt.plot(num_genes, fitness)
plt.xlabel("Number of Satellites Included")
plt.ylabel("Seconds required to reach consensus with PBFT")

# plt.axis('equal')
plt.savefig(save_location+"/ga_results.png")
# plt.show()
