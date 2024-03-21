import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
from prettytable import PrettyTable


max_display_time = 1000

timestep = 30


x = np.load("data/temp/x.npy")

x2 = np.load("data/temp/x2.npy")

sats = []
for p in range(4):
    phases = []
    for i in range(np.shape(x)[1]):
        phase = np.arange(max_display_time)[np.array(x[p,i,:max_display_time],dtype=bool)]
        if len(phase) == 1:
            phases.append(phase[0])
        else:
            phases.append(np.nan)
    sats.append(phases)

sats = np.array(sats)
sats = sats.swapaxes(0,1)
disp = PrettyTable(["Phase 1", "Phase 2", "Phase 3", "Phase 4"])
for sat in sats:
    disp.add_row(sat)


print("##################")
print("Primary satellite:", *np.arange(len(sats))[sats[:,0]==0])
print("All satellites in consensus subset:", *np.arange(len(sats))[~np.isnan(sats[:,0])])
print("Time for consensus:", timestep*round(*sats[sats[:,0]==0,3]), "seconds")
print(disp)
print("##################")


# ####################### Plots ########################


for i in range(len(sats)):
    plt.scatter(sats[i], [i]*4)

prim = 0
 
for j in range(len(sats)):
    if j != prim:
        plt.arrow(sats[prim, 0], prim, (sats[j,0]-sats[prim,0]), j, head_width=0.1, head_length=2,length_includes_head=True)    

for i in range(len(sats)):
    if i != prim:
        for j in range(len(sats)):
            plt.arrow(sats[i, 0], i, (sats[j,1]-sats[i,0]), j, head_width=0.1, head_length=2,length_includes_head=True)    

for i in range(len(sats)):
    for j in range(len(sats)):
        plt.arrow(sats[i, 1], i, (sats[j,2]-sats[i,1]), j, head_width=0.1, head_length=2,length_includes_head=True)    


for i in range(len(sats)):
    if i != prim:
        plt.arrow(sats[i, 2], i, (sats[prim,3]-sats[i,2]), prim, head_width=0.1, head_length=2,length_includes_head=True)    

plt.xlim([0,max_display_time])
# plt.show()