import collections
import subprocess
from queue import Queue
from threading import Thread


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


def draw_game(positions):
    # cleanup positions
    min_x = min(p[0] for p in positions.keys())
    min_y = min(p[1] for p in positions.keys())

    clean_pos = {(x - min_x, y - min_y): v for (x, y), v in positions.items()}
    max_x = max(p[0] for p in clean_pos.keys())
    max_y = max(p[1] for p in clean_pos.keys())

    grid = [([0] * (max_x + 1)).copy() for _ in range(max_y + 1)]
    for pos, val in clean_pos.items():
        grid[max_y - pos[1]][pos[0]] = val

    g = '\n'.join([''.join(map(str, [row for row in col])) for col in grid])
    print(g.replace('0', ' ').replace('1', 'X').replace('2', 'H').replace('3', '=').replace('4', 'o'))


def run():
    # (x, y): color
    # 0 = empty, 1 = wall, 2 = block, 3 = hpaddle, 4 = ball
    positions = collections.defaultdict(lambda: 0)
    score = 0
    out_buf = []

    def get_input():
        draw_game(positions)

        ball_x, ball_y = next((x, y) for ((x, y), t) in positions.items() if t == 4)
        pad_x, pad_y = next((x, y) for ((x, y), t) in positions.items() if t == 3)

        if pad_x < ball_x:
            return '1'
        elif pad_x > ball_x:
            return '-1'
        else:
            return '0'

    def handle_output(out):
        out_buf.append(out)

        if len(out_buf) < 3:
            return
        x, y, tile_id = out_buf
        out_buf.clear()

        if x == -1 and y == 0:
            nonlocal score
            score = tile_id
        else:
            positions[x, y] = tile_id

    computer = Intcode(get_input, handle_output)
    program = list(map(Value, input().split(',')))
    program[0] = Value(2)
    computer.run(program)

    print(score)


if __name__ == '__main__':
    run()
