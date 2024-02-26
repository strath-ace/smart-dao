import matplotlib.pyplot as plt
import numpy as np
things = np.array(np.linspace(200, 2800, int((2800-200)/100+1)), dtype=int)
y = [2.2,3.3,4.8,6.5,7.4,15,17.8,21.6,24.8,33.6,38.7,42,49,55.1,59.6,74.2]

plt.plot(things[:len(y)], y)
# plt.yscale("log")
plt.savefig("test.png")