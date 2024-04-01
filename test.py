import numpy as np
from itertools import combinations

A = np.zeros((15), dtype=int)
B = np.array([3,2,6])

opts = combinations(range(3+2), 3)
res = []
for p in opts:
    print(p)
    res_opt = []
    for i in range(len(p)):
        if i == 0 and p[i] != 0:
            res_opt += [0]*p[i]
            res_opt += [1]*B[i]
        elif i == 0 and p[i] == 0:
            res_opt += [1]*B[i]
        elif i != 0:
            res_opt += [0]*(p[i]-p[i-1])
            res_opt += [1]*B[i]
    if len(res_opt) < A.shape[0]:
        res_opt += [0]*(A.shape[0] - len(res_opt))
    print(res_opt)