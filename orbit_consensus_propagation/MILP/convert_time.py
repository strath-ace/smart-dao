import numpy as np
from pytictoc import TicToc
from itertools import combinations

T = np.load("data/binary_1d.npy")[:,:,:1000]

ticcer = TicToc()
ticcer2 = TicToc()

print(np.shape(T))

sh = np.shape(T)

# print("Start")
# ticcer.tic()
# big = []
# T2 = np.empty((sh[0], sh[1])).tolist()
# for i in range(sh[0]):
#     bigger = []
#     for j in range(sh[1]):
#         if i != j:
#             big = np.array([])
#             for x in range(sh[2]):
#                 big = np.append(big, np.any(np.lib.stride_tricks.sliding_window_view(T[i,j],x), axis=1))
#             bigger.append(big)
#     np.save("data/extra/"+str(i), bigger)
#     print(i)
# ticcer.toc()


print(np.shape(np.lib.stride_tricks.sliding_window_view(T[0,:],[1,100])))