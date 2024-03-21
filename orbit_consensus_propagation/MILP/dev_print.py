import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
from prettytable import PrettyTable

T1 = np.load("data/converted/big.npz")["t"]
# print("New")
print("Shape", np.shape(T1))
print(np.sum(T1), "of", np.prod(np.shape(T1)), "pixels, which is", 100*np.sum(T1)/np.prod(np.shape(T1)),"%")

# T = np.sum(T1, axis=1)

# plt.figure(figsize=(10,10))

# # indx = np.argsort(np.sum(T1, axis=0))
# # plt.imshow(np.rot90(T1[:,indx]), interpolation='none', aspect='auto')

# plt.imshow(np.rot90(T[:,:]), interpolation='none', aspect='auto')

# plt.savefig("temp.png")

# print("First done")
# plt.clf()


# T = np.sum(T1[:,10:20,10:20], axis=2)

# plt.figure(figsize=(10,10))

# plt.imshow(np.rot90(T), interpolation='none', aspect='auto')

# plt.savefig("temp2.png")
# print("Subset done")

# plt.clf()





# T2 = np.load("data/binary_1d.npy")
# spots = [6,9,14,54,12]
# # spots = 10:20

# T = T2[spots][:,spots][:,:,:200].reshape(-1, 200)


# print(np.shape(T))
# plt.figure(figsize=(10,10))
# plt.imshow(T, interpolation='none', aspect='auto')
# plt.savefig("temp4.png")
# plt.clf()







phase = 3
max_time = 200

x = np.load("data/temp/x.npy")

x2 = np.load("data/temp/x2.npy")
# print(x[0,:,:200].tolist())
# print(x2[0,:,:200].tolist())
plt.figure(figsize=(10,10))
plt.imshow(x[phase,:,:max_time], interpolation='none', aspect='auto')
plt.savefig("temp_x.png")
plt.clf()
plt.figure(figsize=(10,10))
plt.imshow(x2[phase,:,:max_time], interpolation='none', aspect='auto')
plt.savefig("temp_x2.png")


phases = []
for p in range(4):
    sats = []
    for i in range(np.shape(x)[1]):
        sat = np.arange(max_time)[np.array(x[p,i,:max_time],dtype=bool)]
        if len(sat) == 1:
            sats.append(sat[0])
        else:
            sats.append(np.nan)
    phases.append(sats)

phases = np.array(phases)
phases = phases.swapaxes(0,1)
disp = PrettyTable(["Phase 1", "Phase 2", "Phase 3", "Phase 4"])
for row in phases:
    disp.add_row(row)
# print(phases)
print(disp)



plt.clf()

spots = [6,9,14,54,12]
T2 = T1[:200,spots][:,:,spots]
T = T2.reshape(200, -1)
print(np.shape(T))

plt.figure(figsize=(10,10))
indx = np.argsort(np.sum(T, axis=0))
T = T.swapaxes(0,1)
# T = T[indx]
plt.imshow(T, aspect='auto', vmin=0, vmax=1)
plt.savefig("temp3.png")
plt.clf()


print("0-1: ", np.arange(max_time)[T2[:,0,1]])
print("0-2: ", np.arange(max_time)[T2[:,0,2]])
print("0-3: ", np.arange(max_time)[T2[:,0,3]])

print("1-2: ", np.arange(max_time)[T2[:,1,2]])
print("1-3: ", np.arange(max_time)[T2[:,1,3]])
print("2-3: ", np.arange(max_time)[T2[:,2,3]])