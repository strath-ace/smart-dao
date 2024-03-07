import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(threshold = np.inf)

# T = np.load("./data/binary_1d.npy")
T = np.load("./binary.npy")
T = np.array(T, dtype=int)

# more_than_zero = np.sum(np.sum(T,axis=2), axis=0) > 0

# T = T[more_than_zero][:,more_than_zero]

indx1 = np.argsort(np.argsort(np.sum(np.sum(T,axis=2), axis=0)))
print(np.sum(np.sum(T[indx1][:,indx1],axis=2), axis=0))


sh = np.shape(T)
print(sh)
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
plt.imshow(flat[:], interpolation='none', aspect='auto') # Replace : with indx to sort by density
# plt.imshow(special[:,:200], interpolation='none', aspect='auto')
plt.savefig("test.png")


plt.clf()

summer = np.sum(T, axis=2)
fig = plt.figure(figsize=(15,15), dpi=500)
fig.tight_layout()
plt.imshow(np.log10(summer), interpolation='none', aspect='auto')
plt.savefig("test2.png")