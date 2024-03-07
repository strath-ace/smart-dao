import numpy as np
import matplotlib.pyplot as plt

z_flat = np.load("data/runtime_results2.npy")

x_coords = np.array(z_flat[:,1], dtype=int)
y_coords = np.array(z_flat[:,2], dtype=int)
z_coords = np.array(z_flat[:,0], dtype=float)

x = np.arange(np.amax(x_coords)+1)
y = np.arange(np.amax(y_coords)+1)

z = np.zeros((np.amax(x_coords)+1, np.amax(y_coords)+1))
z[z == 0] = np.nan
z[x_coords, y_coords] = z_coords
print(np.shape(z))
plt.contourf(x,y , z)
plt.colorbar()
plt.xlim([np.amin(x_coords), np.amax(x_coords)])
plt.xlabel("Minimum Number of Satellites in Consensus")
plt.ylim([np.amin(y_coords), np.amax(y_coords)])
plt.ylabel("Number of Satellites in Subset")
plt.savefig("temp.png")