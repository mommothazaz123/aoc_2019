import itertools
import re
from functools import reduce
from math import gcd


class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.init_x = x
        self.init_y = y
        self.init_z = z
        self.dx = 0
        self.dy = 0
        self.dz = 0

    def gravity_step(self, other):
        for axis in 'xyz':
            if getattr(other, axis) > getattr(self, axis):
                setattr(self, f"d{axis}", getattr(self, f"d{axis}") + 1)
            elif getattr(other, axis) < getattr(self, axis):
                setattr(self, f"d{axis}", getattr(self, f"d{axis}") - 1)

    def velocity_step(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz

    @property
    def pot(self):
        return sum(map(abs, (self.x, self.y, self.z)))

    @property
    def kin(self):
        return sum(map(abs, (self.dx, self.dy, self.dz)))

    def __repr__(self):
        return f"<Moon pos={self.x}, {self.y}, {self.z}; vel={self.dx}, {self.dy}, {self.dz}>"


def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)


def lcmm(*args):
    """Return lcm of args."""
    return reduce(lcm, args)


def step(moons):
    for a, b in itertools.combinations(moons, 2):
        a.gravity_step(b)
        b.gravity_step(a)

    for m in moons:
        m.velocity_step()


def run(fp):
    with open(fp) as f:
        moon_datas = [l for l in f.readlines() if l]

    moons = []
    for moon in moon_datas:
        match = re.match(r'<x=([-+]?\d+), y=([-+]?\d+), z=([-+]?\d+)>', moon)
        x, y, z = map(int, (match.group(1), match.group(2), match.group(3)))
        moons.append(Moon(x, y, z))

    x_cycle = None
    y_cycle = None
    z_cycle = None
    i = 0
    while True:
        print(f"After {i} steps:")
        print('\n'.join([str(m) for m in moons]))
        print(f"Total energy: {sum(m.pot * m.kin for m in moons)}")
        # print(f"Sums: {sum(m.x for m in moons)}, {sum(m.y for m in moons)}, {sum(m.z for m in moons)}")
        print()

        if all(i is not None for i in (x_cycle, y_cycle, z_cycle)):
            break

        if all(m.dx == 0 and m.x == m.init_x for m in moons) and x_cycle is None and i > 0:
            x_cycle = i
        if all(m.dy == 0 and m.y == m.init_y for m in moons) and y_cycle is None and i > 0:
            y_cycle = i
        if all(m.dz == 0 and m.z == m.init_z for m in moons) and z_cycle is None and i > 0:
            z_cycle = i

        step(moons)
        i += 1

    print(f"{x_cycle=} {y_cycle=} {z_cycle=}")
    print(lcmm(x_cycle, y_cycle, z_cycle))


if __name__ == '__main__':
    run(input("File: ") or "in.txt")
