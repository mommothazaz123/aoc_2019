BASE_PATTERN = [0, 1, 0, -1]


def phase(in_list):
    out = []

    for i, elem in enumerate(in_list):
        # build pattern for element
        pattern = []
        for n in BASE_PATTERN:
            pattern.extend([n] * (i + 1))

        while len(pattern) < len(in_list) + 1:
            pattern *= 2

        pattern = pattern[1:]

        # do the mult
        s = 0
        for j, k in zip(in_list, pattern):
            s += j * k

        out.append(abs(s) % 10)

    return out


def run():
    seq = list(map(int, input()))

    for _ in range(100):
        seq = phase(seq)

    print(seq)
    print(''.join(map(str, seq))[:8])


if __name__ == '__main__':
    run()
