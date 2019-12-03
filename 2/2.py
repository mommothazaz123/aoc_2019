# opcode 1:  1 PTRa PTRb PTRc => *PTRc = *PTRa + *PTRb
# opcode 2:  2 PTRa PTRb PTRc => *PTRc = *PTRa * *PTRb
# opcode 99: 99               => halt
# step: pos += 4
import sys


def op1(p, a, b, c):
    p[c] = p[a] + p[b]


def op2(p, a, b, c):
    p[c] = p[a] * p[b]


def run(p):
    pos = 0
    while True:
        opcode = p[pos]

        if opcode == 1:
            op1(p, p[pos + 1], p[pos + 2], p[pos + 3])
        elif opcode == 2:
            op2(p, p[pos + 1], p[pos + 2], p[pos + 3])
        elif opcode == 99:
            break
        else:
            print(f"Invalid opcode: {opcode}")

        pos += 4


if __name__ == '__main__':
    program = list(map(int, input().split(',')))

    for x in range(0, 100):
        for y in range(0, 100):
            pr = program.copy()
            pr[1] = x
            pr[2] = y
            run(pr)
            if pr[0] == 19690720:
                print(f"noun={pr[1]}, verb={pr[2]}")
                sys.exit(0)
