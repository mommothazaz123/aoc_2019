from math import ceil

import numpy as np

BASE_PATTERN = np.array([0, 1, 0, -1])
PATTERN_CACHE = {}


def pattern_for(original_len, elem, offset):
    if elem in PATTERN_CACHE:
        return PATTERN_CACHE[elem]

    patt_row = np.repeat(BASE_PATTERN, (elem + 1))
    patt_row = np.tile(patt_row, ceil(original_len / (elem + 1) * 4))
    patt_row = patt_row[1:original_len + 1]

    # PATTERN_CACHE[elem] = patt_row
    return patt_row[offset:]


def phase(in_arr, original_len, offset):
    out = []
    for i, elem in enumerate(in_arr):
        patt_mat = pattern_for(original_len, i + offset, offset)
        step = np.dot(in_arr, patt_mat)
        out.append(abs(step) % 10)
    return np.array(out)


def run():
    seq = list(map(int, input())) * 10000
    original_len = len(seq)
    print(f"{original_len=}")
    offset = int(''.join(map(str, seq[:7])))
    print(f"{offset=}")

    seq = np.array(seq[offset:])
    print(f"{len(seq)=}")
    print(f"{seq=}")

    for i in range(100):
        seq = phase(seq, original_len, offset)
        print(i)

    print(seq)
    print(''.join(map(str, seq))[:8])


if __name__ == '__main__':
    run()
