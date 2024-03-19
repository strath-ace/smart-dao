import numpy as np
from pytictoc import TicToc

T = np.load("data/binary_1d.npy")[:,:,1:1001]
# WIP CHANGED :1000 to 1:1001

ticcer = TicToc()
ticcer2 = TicToc()

print(np.shape(T))

sh = np.shape(T)

c = 0
all_data = np.zeros((np.sum(np.arange(sh[2]+1)), sh[0], sh[0]), dtype=bool)
ticcer.tic()
for x in range(1,sh[2]+1):
    z = np.array(np.any(np.lib.stride_tricks.sliding_window_view(T,(sh[0],sh[0],x))[0,0], axis=3), dtype=bool)
    all_data[c:c+np.shape(z)[0],:,:] = z
    c += np.shape(z)[0]
    print(str(x)+"/"+str(sh[2]))
ticcer.toc()
print("Saving to file")
np.savez_compressed("data/converted/big", t=all_data)
print("Done")