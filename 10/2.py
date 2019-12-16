import sys
from math import atan2, sqrt, pi
from typing import Set, Tuple


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

    best: Tuple[Tuple[int, int], Set[float]] = sorted(angles.items(), key=lambda i: len(i[1]))[-1]
    best_pos = best[0]
    best_len = len(best[1])
    print(f"Best: {best_pos} with {best_len}")

    # get vaporize list
    vaporized = []
    to_vaporize = asteroids.copy()
    to_vaporize.remove(best_pos)

    while to_vaporize:
        # calculate vaporized this rotation
        this_rotation = {}  # angle: position
        for other in to_vaporize:
            adj, opp = other[0] - best_pos[0], other[1] - best_pos[1]
            angle = -atan2(opp, adj)
            distance = sqrt(adj ** 2 + opp ** 2)
            if angle in this_rotation and distance > sqrt(this_rotation[angle][0] ** 2 + this_rotation[angle][1] ** 2):
                continue
            else:
                this_rotation[angle] = other

        # calculate order of vaporization
        order = []
        for angle, pos in this_rotation.items():
            if angle > pi / 2:
                angle = angle - 2 * pi
            order.append((angle, pos))
        order = sorted(order, key=lambda a: a[0], reverse=True)

        # vaporize
        for angle, pos in order:
            to_vaporize.remove(pos)
            vaporized.append(pos)

    print(vaporized)
    print(f"200th vaporized: {vaporized[199]}")


if __name__ == '__main__':
    run()
