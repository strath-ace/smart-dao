import numpy as np

np.set_printoptions(threshold = np.inf)

T = np.load("binary_1d.npy")
T = np.array(T, dtype=int)

# T[i,j,t]

indx = np.argsort(np.argsort(np.sum(np.sum(T,axis=2), axis=0)))
indx = indx[:10]

T = T[indx][:,indx]

for t in range(np.shape(T)[2]):
    T[:,:,t][T[:,:,t] == 1] = t

T[T == 0] = 999999

# for t in range(np.shape(T)[2]):
#     print(T[:,:,t])


START_TIME = 7
TIMESTEP = 30

ten = np.array(np.round(np.linspace(START_TIME, START_TIME+( 2*14400*TIMESTEP),  2*14400)), dtype=int)
one = np.array(np.round(np.linspace(START_TIME, START_TIME+( 2*1440*TIMESTEP),  2*1440)), dtype=int)

print(ten[:2*1440-1])

if  np.array_equal(one, ten[:2*1440-1]):
    print("true")
else:
    print("false")