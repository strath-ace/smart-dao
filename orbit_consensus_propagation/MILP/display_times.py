import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(threshold = np.inf)

# T = np.load("./data/binary_1d.npy")
T = np.load("./binary.npy")
T = np.array(T, dtype=int)

sh = np.shape(T)

flat = []
special = []
c = 0
for i in range(sh[0]):
    for j in range(sh[1]):
        if j > i:
            flat.append(T[i,j])
            c += 1
            if i in [6,9,14,54] and j in [6,9,14,54]:
                special.append(T[i,j])

flat = np.array(flat)
special = np.array(special)

flat = flat[np.sum(flat,axis=1) > 0]
indx = np.argsort(np.sum(flat, axis=1))

fig = plt.figure(figsize=(15,15), dpi=500)
fig.tight_layout()
plt.imshow(flat[indx,:c], interpolation='none', aspect='auto')
# plt.imshow(special[:,:200], interpolation='none', aspect='auto')
plt.savefig("test.png")