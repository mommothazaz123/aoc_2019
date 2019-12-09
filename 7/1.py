import itertools
import subprocess


def run(program):
    highest = 0
    options = itertools.permutations(range(5))

    for values in options:
        previous_out = 0
        for value in values:
            result = subprocess.run(["python", "intcode.py"],
                                    input=f"{program}\n{value}\n{previous_out}",
                                    capture_output=True,
                                    text=True)
            previous_out = int(result.stdout)

        highest = max(highest, previous_out)
    print(f"Highest: {highest}")


if __name__ == '__main__':
    run(input())
