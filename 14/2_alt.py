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

    surplus = True
    i = 0
    while surplus:
        produce_fuel()
        i += 1
        surplus = {k: produced[k] - wanted[k] for k in produced if produced[k] > wanted[k] and wanted[k]}
        if not i % 1000:
            print(i)

    consumed_per = wanted['ORE']
    print(f"Every {i} fuel we consume {consumed_per} ore, with no surplus")
    max_eff = (1000000000000 // consumed_per) * i
    remaining_ore = 1000000000000 - (consumed_per * max_eff / i)
    print(f"{max_eff=}, {remaining_ore=}")

    produced.clear()
    wanted.clear()

    while wanted["ORE"] < remaining_ore:
        produce_fuel()

    print(max_eff + produced['FUEL'] - 1)


if __name__ == '__main__':
    run(input("File: ") or 'in.txt')
