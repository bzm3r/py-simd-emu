import numpy as np

# count trailing zeros
def ctz(x):
  if x == 0: return 32
  r = 0

  # if x % 2 is 0, then the last bit must be 0 (last bit is 2^0 = 1)
  while (x % 2) == 0:
    r += 1
     # shift bits left by 1
    x >>= 1
  return r

# count leading zeros
def clz(x):
    # start at 31, go until -1, with step -1
    for k in range(31, -1, -1):
        # check if bit at position k is non-zero
        if x & (1 << k):
            return 31 - k
    return 32

# count number of ones (population count)
def popcnt(x):
    r = 0
    for k in range(32):
        # check if bit at position k is non-zero
        if x & (1 << k):
            r += 1
    return r

# climbing sum
def subgroup_inclusive_add(xs):
    sum = 0
    result = []
    for x in xs:
        sum += x
        result.append(sum)
    return result

# bit-wise or of all x
def subgroup_or(xs):
    result = 0
    for x in xs:
        result |= x
    return result

# subgroup ballot, with predicate is is b == 1
def subgroup_ballot(bs):
    result = 0
    for (i, b) in enumerate(bs):
        if b:
            result |= 1 << i
    return result

def subgroup_shuffle_xor(caller_tid, values, mask):
    rd_tid = caller_tid^mask
    return values[rd_tid]

