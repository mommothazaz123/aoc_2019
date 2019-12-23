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

    def produce_fuel():
        wanted["FUEL"] += 1
        running = True
        while running:
            running = False
            for chem, num in wanted.copy().items():
                if produced[chem] < num and chem in reactions:
                    running = True
                    reaction = reactions[chem]
                    execute(reaction)

    last_avg = 1
    ores_consumed = []
    while True:
        ore_before = wanted["ORE"]
        produce_fuel()
        ore_after = wanted["ORE"]
        ores_consumed.append(ore_after - ore_before)
        avg = sum(ores_consumed) / len(ores_consumed)
        print(avg)
        if 1000000000000 // avg == 1000000000000 // last_avg:
            break
        last_avg = avg
    print(1000000000000 // last_avg)


if __name__ == '__main__':
    run(input("File: ") or 'in.txt')
