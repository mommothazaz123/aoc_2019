import itertools
import re


class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
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

    for i in range(1001):
        print(f"After {i} steps:")
        print('\n'.join([str(m) for m in moons]))
        print(f"Total energy: {sum(m.pot * m.kin for m in moons)}")
        print()

        step(moons)


if __name__ == '__main__':
    run(input("File: ") or "in.txt")
