# opcode 1:  1 VARa VARb PTRc => *PTRc = VARa + VARb
# opcode 2:  2 VARa VARb PTRc => *PTRc = VARa * VARb
# opcode 3:  3 PTRa           => *PTRa = input()
# opcode 4:  4 VARa           => output(VARa)
# opcode 5:  5 VARa VARb      => *PC   = VARb if VARa != 0
# opcode 6:  6 VARa VARb      => *PC   = VARb if VARa == 0
# opcode 7:  7 VARa VARb PTRc => *PTRc = VARa < VARb
# opcode 8:  8 VARa VARb PTRc => *PTRc = VARa == VARb
# opcode 99: 99               => halt
# step: pos += 4
import sys

OPERATIONS = {}


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


class Halt(Exception):
    pass


# operations
def operation(opcode, args):
    def wrapper(func):
        OPERATIONS[opcode] = (func, args)
        return func

    return wrapper


@operation(1, args=3)
def op1(a, b, c):
    c.n = a.n + b.n


@operation(2, args=3)
def op2(a, b, c):
    c.n = a.n * b.n


@operation(3, args=1)
def op3(a):
    a.n = int(input())


@operation(4, args=1)
def op4(a):
    print(a.n)


@operation(5, args=2)
def op5(a, b):
    if a.n != 0:
        pos.n = b.n


@operation(6, args=2)
def op6(a, b):
    if a.n == 0:
        pos.n = b.n


@operation(7, args=3)
def op7(a, b, c):
    c.n = int(a.n < b.n)


@operation(8, args=3)
def op8(a, b, c):
    c.n = int(a.n == b.n)


@operation(99, args=0)
def op99():
    raise Halt


# runner
def run(p):
    while True:
        # print(f"{pos}: {p}")
        instruction = p[pos.n]
        opcode = instruction.n % 100

        if opcode not in OPERATIONS:
            raise RuntimeError(f"Unknown operation: {opcode} (pc={pos.n})")

        op, nargs = OPERATIONS[opcode]
        args = []
        for i in range(nargs):
            # 0 = position mode, 1 = immediate mode
            mode = (instruction.n // (10 ** (i + 2)) % 10)
            if mode == 0:
                args.append(p[p[pos.n + i + 1].n])  # value at address=argument i
            else:
                args.append(Value(p[pos.n + i + 1].n))  # value=argument i

        try:
            op(*args)
        except Halt:
            break
        pos.step(nargs + 1)


if __name__ == '__main__':
    program = list(map(Value, input().split(',')))
    pos = PC()
    run(program)
