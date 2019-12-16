import collections
import subprocess

DIRECTIONS = ['up', 'right', 'down', 'left']  # turn right:


def run(program):
    # (x, y): color
    # black = 0, white = 1
    positions = collections.defaultdict(lambda: 0)

    position = (0, 0)
    direction = 0  # to turn right, direction = (direction + 1) % 4

    proc = subprocess.Popen(["python", "intcode.py"], 1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            text=True)
    proc.stdin.write(f"{program}\n")
    proc.stdin.flush()

    while proc.poll() is None:
        # read
        proc.stdin.write(f"{positions[position]}\n")
        proc.stdin.flush()
        try:
            color = int(proc.stdout.readline().strip())
            turn = int(proc.stdout.readline().strip())
        except:
            break

        # paint
        positions[position] = color

        # move
        direction = (direction + (2 * turn - 1)) % 4
        if direction == 0:
            position = (position[0], position[1] + 1)
        elif direction == 1:
            position = (position[0] + 1, position[1])
        elif direction == 2:
            position = (position[0], position[1] - 1)
        else:
            position = (position[0] - 1, position[1])

    print(len(positions))


if __name__ == '__main__':
    run(input())
