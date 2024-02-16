import matplotlib.pyplot as plt
import numpy as np
import os

SAVE_DIR = "data_icsmd_1day"

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("Sat Data not setup, run get_active_tle.py first")

for_view = np.load(save_location+"/all_combs.npy")
si = np.shape(for_view)

fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")

x_li = np.array(np.linspace(0,si[0]-1, si[0]), dtype=int)
y_li = np.array(np.linspace(0,si[1]-1, si[1]), dtype=int)
x = []
y = []
z = []
for xi in x_li:
    for yi in y_li:
        for zi in for_view[xi,yi]:
            x.append(xi)
            y.append(yi)
            z.append(zi)

z = np.array(z)
# Just make it log10 between 0 and 1
z = np.log10(z)/(np.amax(np.log10(z[np.logical_not(np.isnan(np.log10(z)))])))


ax.scatter3D(x, y, z)
plt.savefig(save_location+"/scatter.png")


plt.clf()
flatter = (np.sum(np.logical_not(np.isnan(for_view)), axis=2))
indx = np.flip(np.argsort(np.sum(flatter, axis=0)))
# print(indx)
# print("PLOT",np.shape(flatter))
flatter = flatter[indx]
flatter = flatter[:,indx]
plt.imshow(np.log10(np.log10(flatter)))
plt.gca().invert_yaxis()
plt.colorbar()
plt.savefig(save_location+"/imshow.png")