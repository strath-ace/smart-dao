import numpy as np
import matplotlib.pyplot as plt

from common import *


data = load_json("with_without.json")

fig = plt.figure(figsize=(7.7,4), layout="constrained")

data_all = []
for i in range(20):
    try:
        data_i = np.array(data["day_"+str(i)])
        data_all.append(data_i)
        
    except:
        pass

data_all = np.array(data_all)
for i in range(len(data_all)):
    plt.plot(np.arange(len(data_all[i,:,1,0]))+1, data_all[i,:,1,0]-data_all[i,:,0,0], c="black", alpha=0.4)


data_meaned = np.mean(data_all,axis=0)
plt.plot(np.arange(len(data_meaned[:,1,0]))+1, data_meaned[:,1,0]-data_meaned[:,0,0], c="red", alpha=1)

plt.title("Difference in number of satellites that can participate after simulated satellite added")
plt.ylabel("Difference in number of satellites")
plt.xlabel("Days to reach consensus")
plt.xticks([0,2.5,5,7.5,10], [0,0.25,0.5,0.75,1])
plt.savefig("figures/with_without.png")
plt.clf()