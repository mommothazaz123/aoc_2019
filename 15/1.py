# opcode 1:  1 VARa VARb PTRc => *PTRc = VARa + VARb
# opcode 2:  2 VARa VARb PTRc => *PTRc = VARa * VARb
# opcode 3:  3 PTRa           => *PTRa = input()
# opcode 4:  4 VARa           => output(VARa)
# opcode 5:  5 VARa VARb      => PC    = VARb if VARa != 0
# opcode 6:  6 VARa VARb      => PC    = VARb if VARa == 0
# opcode 7:  7 VARa VARb PTRc => *PTRc = VARa < VARb
# opcode 8:  8 VARa VARb PTRc => *PTRc = VARa == VARb
# opcode 9:  9 VARa           => relbase = relbase + VARa
# opcode 99: 99               => halt
# step: pos += 4
import collections


class Value:
    def __init__(self, n):
        self.n = int(n)

    def __repr__(self):
        return str(self.n)


class PC:
    def __init__(self):
        self._n = 0
        self.allow_step = True

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        self.allow_step = False
        self._n = value

    def step(self, count):
        if self.allow_step:
            self._n += count
        else:
            self.allow_step = True


class Intcode:
    def __init__(self, i=None, o=None):
        self.pc = PC()
        self.running = True
        self.relbase = 0
        self.i = i or input
        self.o = o or print

        self.OPERATIONS = {
            1: (self.op1, 3),
            2: (self.op2, 3),
            3: (self.op3, 1),
            4: (self.op4, 1),
            5: (self.op5, 2),
            6: (self.op6, 2),
            7: (self.op7, 3),
            8: (self.op8, 3),
            9: (self.op9, 1),
            99: (self.op99, 0),
        }

    def op1(self, a, b, c):
        c.n = a.n + b.n

    def op2(self, a, b, c):
        c.n = a.n * b.n

    def op3(self, a):
        a.n = int(self.i())

    def op4(self, a):
        self.o(a.n)

    def op5(self, a, b):
        if a.n != 0:
            self.pc.n = b.n

    def op6(self, a, b):
        if a.n == 0:
            self.pc.n = b.n

    def op7(self, a, b, c):
        c.n = int(a.n < b.n)

    def op8(self, a, b, c):
        c.n = int(a.n == b.n)

    def op9(self, a):
        self.relbase += a.n

    def op99(self):
        self.running = False

    # runner
    def run(self, p):
        p = p + [Value(0) for _ in range(1000)]
        self.running = True
        self.relbase = 0

        while self.running:
            # print(f"{pos}: {p}")
            instruction = p[self.pc.n]
            opcode = instruction.n % 100

            if opcode not in self.OPERATIONS:
                raise RuntimeError(f"Unknown operation: {opcode} (pc={self.pc})")

            op, nargs = self.OPERATIONS[opcode]
            args = []
            for i in range(nargs):
                # 0 = position mode, 1 = immediate mode, 2 = relative mode
                mode = (instruction.n // (10 ** (i + 2)) % 10)
                if mode == 0:
                    args.append(p[p[self.pc.n + i + 1].n])  # value at address=argument i
                elif mode == 1:
                    args.append(Value(p[self.pc.n + i + 1].n))  # value=argument i
                else:
                    args.append(p[p[self.pc.n + i + 1].n + self.relbase])  # value at address=relbase+argument i

            op(*args)
            self.pc.step(nargs + 1)


def get_around(pos):
    x, y = pos
    return [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]  # n, s, w, e


# def dfs(pos, visited=None):
#     if visited is None:
#         visited = set()
#
#     if positions[pos] == 2:
#         return 0
#
#     for new_pos in get_around(pos):
#         if new_pos in visited:
#             continue
#         visited.add(new_pos)
#         result = dfs(new_pos, visited)
#         if result is not None:
#             return result + 1


def run():
    # movement: 1=n, 2=s, 3=w, 4=e
    # explored: -1=unknown, 0=wall, 1=empty, 2=oxy
    positions = collections.defaultdict(lambda: -1, [((0, 0), 0)])
    current = (0, 0)
    new_pos = None
    visited = {(0, 0)}
    stack = [(0, 0)]

    def get_movement():
        nonlocal new_pos
        new_pos = next((p for p in get_around(current) if p not in visited), None)
        if new_pos is None:
            del stack[-1]
            new_pos = stack[-1]
        return get_around(current).index(new_pos) + 1

    def process_movement(result):
        nonlocal current
        visited.add(new_pos)
        positions[new_pos] = result
        if result != 0:
            current = new_pos
            if new_pos != stack[-1]:
                stack.append(new_pos)
        if result == 2:
            raise RuntimeError()
        print(positions)

    computer = Intcode(i=get_movement, o=process_movement)
    program = list(map(Value, input().split(',')))
    try:
        computer.run(program)
    except RuntimeError:
        print(current)
        print(len(stack))


if __name__ == '__main__':
    run()
