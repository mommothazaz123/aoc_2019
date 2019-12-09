import itertools
import subprocess
import time


def run_values(program, values):
    print("foo")
    amps = []
    previous = "0"
    for value in values:
        proc = subprocess.Popen(["python", "intcode.py"], 1,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                text=True)
        proc.stdin.write(f"{program}\n")
        proc.stdin.flush()
        proc.stdin.write(f"{value}\n")
        proc.stdin.flush()
        amps.append(proc)

    while amps[0].poll() is None:
        print("loop")
        for proc in amps:
            proc.stdin.write(f"{previous}\n")
            proc.stdin.flush()
            previous = proc.stdout.readline().strip()
        time.sleep(0.05)
    return int(previous)


def run(program):
    highest = 0
    options = itertools.permutations(range(5, 10))

    for values in options:
        out = run_values(program, values)
        highest = max(highest, out)
    print(f"Highest: {highest}")


if __name__ == '__main__':
    run(input())

# 3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
# 3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10