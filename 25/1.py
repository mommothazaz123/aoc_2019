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
import functools
import itertools


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


class ASCIIIntcode(Intcode):
    def __init__(self, *args, o=None, **kwargs):
        o = o or functools.partial(print, end='')
        super().__init__(*args, o=o, **kwargs)
        self._in_buf = []

    def op3(self, a):
        if not self._in_buf:
            self._in_buf.extend([ord(c) for c in self.i()])
            self._in_buf.append(10)
        a.n = int(self._in_buf.pop(0))

    def op4(self, a):
        self.o(chr(a.n))


ITEMS = [
    "loom",
    "spool of cat6",
    "fixed point",
    "candy cane",
    "weather machine",
    "ornament",
    "wreath",
    "shell"
]

INITIAL_REPLAY = [
    "east",
    "take loom",
    "south",
    "take ornament",
    "west",
    "north",
    "take candy cane",
    "south",
    "east",
    "north",
    "east",
    "take fixed point",
    "north",
    "take spool of cat6",
    "north",
    "take weather machine",
    "south",
    "west",
    "take shell",
    "east",
    "south",
    "west",
    "west",
    "north",
    "take wreath",
    "north",
    "east",
    # drop all items
]


def run():
    state = 0
    held_items = [
        "loom",
        "spool of cat6",
        "fixed point",
        "candy cane",
        "weather machine",
        "ornament",
        "wreath",
        "shell"
    ]
    buf = []

    def do_input():
        if buf:
            return buf.pop(0)

        nonlocal state
        if state == -1:
            return input()

        if state == 0:
            if INITIAL_REPLAY:
                return INITIAL_REPLAY.pop(0)
            else:
                state = 1

        if state == 1:  # drop all items
            if held_items:
                return f"drop {held_items.pop(0)}"
            else:
                state = 2
                return do_input()

        if state >= 2:
            for comb in itertools.combinations(ITEMS, state - 1):
                buf.extend(f"take {i}" for i in comb)
                buf.append("south")
                buf.extend(f"drop {i}" for i in comb)
            state += 1
            return do_input()

    computer = ASCIIIntcode(i=do_input)
    with open('in.txt') as f:
        program = list(map(Value, f.read().strip().split(',')))
    computer.run(program)


if __name__ == '__main__':
    run()
