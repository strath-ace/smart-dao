import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt

T1 = np.load("data/converted/big.npz")["t"]
# print("New")
print("Shape", np.shape(T1))
print(np.sum(T1), "of", np.prod(np.shape(T1)), "pixels, which is", 100*np.sum(T1)/np.prod(np.shape(T1)),"%")

T = np.sum(T1, axis=1)

plt.figure(figsize=(10,10))

# indx = np.argsort(np.sum(T1, axis=0))
# plt.imshow(np.rot90(T1[:,indx]), interpolation='none', aspect='auto')

plt.imshow(np.rot90(T[:,:]), interpolation='none', aspect='auto')

plt.savefig("temp.png")

print("First done")
plt.clf()


T = np.sum(T1[:,10:20,10:20], axis=2)

plt.figure(figsize=(10,10))

plt.imshow(np.rot90(T), interpolation='none', aspect='auto')

plt.savefig("temp2.png")
print("Subset done")