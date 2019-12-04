def get_points():
    points = []
    pos = (0, 0)

    wire = input()
    path = wire.split(',')

    for ins in path:
        dir, num = ins[:1], int(ins[1:])
        if dir == 'U':
            step = lambda x, y: (x, y + 1)
        elif dir == 'D':
            step = lambda x, y: (x, y - 1)
        elif dir == 'L':
            step = lambda x, y: (x - 1, y)
        elif dir == 'R':
            step = lambda x, y: (x + 1, y)
        else:
            raise RuntimeError(f"Unknown dir {dir}")

        for _ in range(num):
            pos = step(*pos)
            points.append(pos)

    return points


def run():
    points1 = get_points()
    points2 = get_points()
    intersections = set(points1).intersection(set(points2))

    print(f"Intersections: {intersections}")
    print(f"Min distance: {min(sum(map(abs, pts)) for pts in intersections)}")

    distances = []

    for inter in intersections:
        dist1 = points1.index(inter) + 1
        dist2 = points2.index(inter) + 1
        distances.append((inter, dist1 + dist2))

    print(f"With distances: {distances}")
    fewest, steps = sorted(distances, key=lambda d: d[1])[0]
    print(f"The fewest combined steps is {steps} at {fewest}")


if __name__ == '__main__':
    run()
