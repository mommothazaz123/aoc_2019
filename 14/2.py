import collections


class Dependency:
    def __init__(self, chemical, number):
        self.chemical = chemical
        self.number = number

    @classmethod
    def parse(cls, s):
        num, chem = s.split(' ')
        return cls(chem, int(num))

    def __str__(self):
        return f"{self.number} {self.chemical}"


class Reaction:
    def __init__(self, outputs, inputs):
        self.outputs = outputs
        self.inputs = inputs

    @classmethod
    def parse(cls, s):
        ins, outs = s.split(" => ")
        return cls([Dependency.parse(c) for c in outs.split(', ')], [Dependency.parse(c) for c in ins.split(', ')])

    def __str__(self):
        return f"{', '.join([str(d) for d in self.inputs])} => {', '.join([str(d) for d in self.outputs])}"

    def __repr__(self):
        return str(self)


def run(fp):
    reactions = {}  # output (str): Reaction

    with open(fp) as f:
        reaction_data = [l.strip() for l in f.readlines() if l]

    for reaction in map(Reaction.parse, reaction_data):
        for out in reaction.outputs:
            reactions[out.chemical] = reaction

    print(reactions)

    produced = collections.defaultdict(lambda: 0)
    wanted = collections.defaultdict(lambda: 0)

    def execute(r):
        for dep in r.inputs:
            wanted[dep.chemical] += dep.number
        for dep in r.outputs:
            produced[dep.chemical] += dep.number

    def produce(x):
        wanted[x] += 1
        running = True
        while running:
            running = False
            for chem, num in wanted.copy().items():
                if produced[chem] < num and chem in reactions:
                    running = True
                    reaction = reactions[chem]
                    execute(reaction)

    produce("FUEL")
    max_surplus = {k: produced[k] - wanted[k] for k in produced if produced[k] > wanted[k]}
    max_ore = wanted['ORE']
    print(f"Max ore per fuel: {max_ore}")
    print(f"{max_surplus=}")

    def calculate_surplus(dedicated):
        max_fuel = dedicated // max_ore
        remaining_ore = 1000000000000 - (max_ore * max_fuel)
        total_surplus = {k: v * max_fuel for k, v in max_surplus.items()}
        total_surplus["ORE"] = remaining_ore
        return max_fuel, total_surplus

    def run_dedicated(dedicated):
        max_fuel, total_surplus = calculate_surplus(dedicated)

        produced.clear()
        wanted.clear()

        produced.update(total_surplus)
        i = 0
        while all(wanted[k] <= produced[k] for k in produced):
            produce("FUEL")
            i += 1
            if not i % 1000:
                print(i)

        return ({k: produced[k] - wanted[k] for k in produced if produced[k] > wanted[k]},
                max_fuel + produced["FUEL"] - 1)

    i = 1000000000000
    while True:
        max_fuel, total_surplus = calculate_surplus(i)
        if total_surplus.pop("ORE") < sum(total_surplus.values()) * max_ore:
            i -= 1000000
        else:
            break

    print(i)
    print(calculate_surplus(i))

    print(run_dedicated(i))


if __name__ == '__main__':
    run(input("File: ") or 'in.txt')
