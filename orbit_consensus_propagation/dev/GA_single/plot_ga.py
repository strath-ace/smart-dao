import matplotlib.pyplot as plt
import numpy as np
import os
from generic import *




# Create save location if not already exist
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

print("Graphing GA Fitness")

ga_data = np.asarray(np.array(csv_input(save_location+"/ga_results.csv")), dtype="float")


plt.plot(ga_data[:,0])
plt.yscale("log")
# plt.axis('equal')
plt.savefig(save_location+"/ga_fitness.png")
# plt.show()
plt.show()
