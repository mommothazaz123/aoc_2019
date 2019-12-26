def run():
    positions = []

    fp = input() or '1_in.txt'
    with open(fp) as f:
        for line in f.readlines():
            positions.append(list(line.strip()))

    total = 0

    for i, row in enumerate(positions):
        for j, col in enumerate(row):
            if (0 < i < len(positions) - 1
                    and 0 < j < len(row) - 1
                    and col == '#'
                    and positions[i - 1][j] == '#'
                    and positions[i + 1][j] == '#'
                    and positions[i][j - 1] == '#'
                    and positions[i][j + 1] == '#'):
                total += i * j

    print(total)


if __name__ == '__main__':
    run()
