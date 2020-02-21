from simd_intrinsics import *

def is_last_helper(k0, tix, ns):
    subgroup_size = len(ns)
    if ns[tix] >= (k0 + 1) and ns[tix] < (k0 + 1) + subgroup_size:
        return 1 << (ns[tix] - k0 - 1)
    else:
        return 0

def iter_backdrop_mask(is_last):
    m = is_last
    mask = is_last ^ (is_last - 1)
    print("first:", hex(mask))
    while m:
        k = ctz(m)
        mask = is_last ^ (is_last - (2 << k))
        print("next:", hex(mask & 0xffffffff))
        m &= m - 1

def simulate_kernel2(subgroup_size, ns):
    for i0 in range(0, len(ns), subgroup_size):
        n = [ns[i0 + tix] if i0 + tix < len(ns) else 0 for tix in range(subgroup_size)]
        prefix_n = subgroup_inclusive_add(n)
        print('n:', n)
        print('prefix_n:', prefix_n)
        sum_n = prefix_n[-1]
        ilast = 0
        jlast = 0
        for k0 in range(0, sum_n, subgroup_size):
            is_last = subgroup_or([is_last_helper(k0, tix, prefix_n) for tix in range(subgroup_size)])
            print('is_last:', bin(is_last))
            delta_i = [0 if tix == 0 else popcnt(is_last << (32 - tix)) for tix in range(subgroup_size)]
            i_inv = [ilast + delta_i[tix] for tix in range(subgroup_size)]
            print('i_inv:', i_inv)
            j_inv = [jlast + tix if delta_i[tix] == 0 else clz(is_last << (32 - tix)) for tix in range(subgroup_size)]
            print('j_inv:', j_inv)

            ilast += popcnt(is_last)
            jlast = j_inv[-1] + 1

simulate_kernel2(8, [2, 3, 5, 1, 1, 1, 1, 1, 1])