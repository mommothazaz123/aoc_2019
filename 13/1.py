import collections
import subprocess

DIRECTIONS = ['up', 'right', 'down', 'left']  # turn right:


def run(program):
    # (x, y): color
    # 0 = empty, 1 = wall, 2 = block, 3 = hpaddle, 4 = ball
    positions = collections.defaultdict(lambda: 0)

    proc = subprocess.Popen(["python", "intcode.py"], 1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            text=True)
    proc.stdin.write(f"{program}\n")
    proc.stdin.flush()

    while proc.poll() is None:
        try:
            x = int(proc.stdout.readline().strip())
            y = int(proc.stdout.readline().strip())
            tile_id = int(proc.stdout.readline().strip())
        except:
            break

        positions[x, y] = tile_id

    print(positions)
    print(sum(1 for b in positions.values() if b == 2))


if __name__ == '__main__':
    run(input())
