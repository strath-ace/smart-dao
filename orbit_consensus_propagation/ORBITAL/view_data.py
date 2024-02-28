import numpy as np
import os
import matplotlib.pyplot as plt

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

data = np.load(save_location+"/sim_pos.npy")

print(np.shape(data))

fig = plt.figure(figsize=(10,10), dpi=300).add_subplot(projection='3d')

# for i in range(np.shape(data)[0]):
for i in range(np.shape(data)[0]):
    plt.plot(data[i,:,0], data[i,:,1], data[i,:,2])

plt.xlim([-8000,8000])
plt.ylim([-8000,8000])
fig.set_zlim3d([-8000,8000])

# fig.set_aspect('auto')

plt.savefig(save_location+"/temp.png")
# plt.show()