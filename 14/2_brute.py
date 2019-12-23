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
    wanted = collections.defaultdict(lambda: 0, FUEL=1)

    def execute(r):
        for dep in r.inputs:
            wanted[dep.chemical] += dep.number
        for dep in r.outputs:
            produced[dep.chemical] += dep.number

    while wanted["ORE"] < 1000000000000:
        if wanted["FUEL"] == produced["FUEL"]:
            wanted["FUEL"] += 1
            print(wanted['ORE'])
            print(produced["FUEL"])

        for chem, num in wanted.copy().items():
            if produced[chem] < num and chem in reactions:
                reaction = reactions[chem]
                execute(reaction)

    print(wanted['ORE'])
    print(produced["FUEL"])


if __name__ == '__main__':
    run(input("File: ") or 'in.txt')
