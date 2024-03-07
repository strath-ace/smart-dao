import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(-10,10,1000)
y = 1 - 1/(1+np.exp(-x))

plt.plot(x,y)
plt.savefig("tester.png")