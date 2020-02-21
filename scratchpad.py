from simd_intrinsics import *
import numpy as np
from copy import deepcopy

# def is_last_helper(k0, tix, ns):
#     subgroup_size = len(ns)
#     if ns[tix] >= (k0 + 1) and ns[tix] < (k0 + 1) + subgroup_size:
#         return 1 << (ns[tix] - k0 - 1)
#     else:
#         return 0
#
# subgroup_size = 8
# num_ns = np.random.choice(np.arange(4, 8) + 1)
# ns = np.random.choice(np.arange(8) + 1, num_ns, replace=True)
#
# for i0 in range(0, num_ns, subgroup_size):
#     ms = []
#     for tix in range(subgroup_size):
#         if i0 + tix < num_ns:
#             ms.append(ns[i0 + tix])
#         else:
#             ms.append(0)
#
#     prefix_ms = subgroup_inclusive_add(ms)
#     sum_m = prefix_ms[-1]
#     for k0 in range(0, sum_m, subgroup_size):
#         ps = []
#         for tix in range(subgroup_size):
#             ps.append(is_last_helper(k0, tix, prefix_ms))
#         is_last = subgroup_or(ps)
#

def bnot(n, nbits):
    return (1 << nbits) - 1 - n

def blshift(n, s, nbits):
    return int('0b' + bin(n << s)[2:][-nbits:], 2)

def brshift(n, s, nbits):
    return int('0b' + bin(n >> s)[2:][-nbits:], 2)

def shuffle_round(tix, values, m, s, nbits):
    b = subgroup_shuffle_xor(tix, values, s)
    a = values[tix]
    p = tix & s
    if (tix & s) == 0:
        c = blshift(b, s, nbits)
    else:
        m = bnot(m, nbits)
        c = brshift(b, s, nbits)
    q = a & m
    r = c & bnot(m, nbits)
    return (a & m) | (c & bnot(m, nbits))

np.random.seed(200)
bm_size = 4
#bm = np.random.choice([0, 1], (bm_size, bm_size))
bm = np.array([[1, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [1, 0, 0, 1]])

def gen_ms(bm_size):
    assert(bm_size % 2 == 0)
    s = int(bm_size/2)
    rs = []
    while s > 0:
        c = 0
        m = ''
        for i in range(int(bm_size/s)):
            m += str(c) * s
            c = int(not c)
        rs.append((s, int('0b' + m, 2)))
        s = int(s/2)

    return rs

print(gen_ms(bm_size))
sbm = bm_to_sbm(bm)

itbm = [int(bs, 2) for bs in sbm]
print(itbm)
for s, m in gen_ms(bm_size):
    itbm = [shuffle_round(tix, itbm, m, s, bm_size) for tix in range(bm_size)]
    print("itbm:", itbm)

tsbm = ["0"*(bm_size - len(x)) + x for x in [bin(y)[2:] for y in itbm]]
tbm = sbm_to_bm(tsbm)
print(np.all(np.transpose(bm) == tbm))
