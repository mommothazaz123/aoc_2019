import sys
from math import atan2


def run():
    # load asteroids
    with open(sys.argv[1]) as f:
        grid = f.read().strip()

    asteroids = []

    for y, row in enumerate(grid.split('\n')):
        for x, pos in enumerate(row):
            if pos == '#':
                asteroids.append((x, y))

    # print(f"{asteroids=}")

    # get angles
    angles = {}  # asteroid: set(angles)

    for asteroid in asteroids:
        angles[asteroid] = set()
        for other in asteroids:
            if other is asteroid:
                continue
            adj, opp = other[0] - asteroid[0], other[1] - asteroid[1]
            angle = atan2(opp, adj)
            angles[asteroid].add(angle)

    best_pos, best_angles = sorted(angles.items(), key=lambda i: len(i[1]))[-1]
    best_len = len(best_angles)
    print(f"Best: {best_pos} with {best_len}")


if __name__ == '__main__':
    run()
