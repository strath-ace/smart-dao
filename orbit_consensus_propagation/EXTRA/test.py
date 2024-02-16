from itertools import combinations
import numpy as np
 
items = np.array(np.linspace(1, 6, 6), dtype=int)
comb = combinations(items, 3) 
comb = list(comb)
comb_all = []
for i in range(1, 6):
    for co in comb:
        if i not in co:
            comb_all.append(np.append([i],co))
comb = np.array(comb_all)

print(np.shape(comb))

# no_repeat_comb = []
# for item in comb:
#     passed = True
#     for i in range(1, len(item)):
#         if item[i-1] == item[i]:
#             passed = False
#     if passed:
#         no_repeat_comb.append(item)

# print(len(comb))
# print(len(no_repeat_comb))

# print(no_repeat_comb)

# big = 0

# for i in range()


