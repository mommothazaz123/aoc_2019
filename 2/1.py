# opcode 1:  1 PTRa PTRb PTRc => *PTRc = *PTRa + *PTRb
# opcode 2:  2 PTRa PTRb PTRc => *PTRc = *PTRa * *PTRb
# opcode 99: 99               => halt
# step: pos += 4

def op1(p, pos):
    p[p[pos + 3]] = p[p[pos + 1]] + p[p[pos + 2]]


def op2(p, pos):
    p[p[pos + 3]] = p[p[pos + 1]] * p[p[pos + 2]]


def run(p):
    pos = 0
    while True:
        opcode = p[pos]

        if opcode == 1:
            op1(p, pos)
        elif opcode == 2:
            op2(p, pos)
        elif opcode == 99:
            break
        else:
            print(f"Invalid opcode: {opcode}")

        pos += 4

    print(p)


if __name__ == '__main__':
    while True:
        program = list(map(int, input().split(',')))
        run(program)
