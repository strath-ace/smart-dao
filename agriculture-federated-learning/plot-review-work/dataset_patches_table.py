import numpy as np


num_patches = 5990


split_fed = 0.8
split_cent = 0.2

split_train = 0.9
split_valid = 0.1

for i in [2,4,8,16,32,64,128,256]:
    fed = num_patches*split_fed
    cent = num_patches*split_cent
    train = fed*split_train
    valid = fed*split_valid
    data = np.array([i, round(train/i), round(valid/i), round(cent)],dtype=str)
    print(" & ".join(data), "\\\\")