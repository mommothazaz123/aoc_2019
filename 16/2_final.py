def run():
    seq = list(map(int, input())) * 10000
    original_len = len(seq)
    print(f"{original_len=}")
    offset = int(''.join(map(str, seq[:7])))
    print(f"{offset=}")

    seq = seq[offset:]
    print(f"{len(seq)=}")
    # print(f"{seq=}")

    for i in range(100):
        sums = {0: 0}

        for j in range(1, len(seq) + 1):
            sums[j] = seq[-j] + sums[j - 1]

        seq = [abs(n) % 10 for n in reversed(sums.values())][:-1]
        print(i)

    print(seq)
    print(''.join(map(str, seq))[:8])


if __name__ == '__main__':
    run()
