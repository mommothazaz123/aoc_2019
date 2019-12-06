class Node:
    def __init__(self, name, parent):
        self.id = name
        self.parent = parent
        self.children = []

    @property
    def leaves(self):
        return self.children + [self.parent]

    def __repr__(self):
        return self.id


nodes = {}


def get_node(name):
    if name in nodes:
        return nodes[name]
    node = Node(name, None)
    nodes[name] = node
    return node


# run
with open("in.txt") as f:
    lines = [l.strip() for l in f.readlines() if l.strip()]

for line in lines:
    ed, er = line.split(')')
    orbited, orbiter = get_node(ed), get_node(er)
    orbiter.parent = orbited
    orbited.children.append(orbiter)


def depth(node):
    i = 0
    while node.parent:
        i += 1
        node = node.parent
    return i


print(sum(depth(node) for node in nodes.values()))  # end part 1


def dfs(origin, destination, visited=None):
    if visited is None:
        visited = []

    if origin is destination:
        return visited

    leaves = [l for l in origin.leaves if l not in visited]
    if not leaves:
        return None

    for leaf in leaves:
        if (path := dfs(leaf, destination, visited + [origin])) is not None:
            return path


print(len(dfs(nodes['YOU'].parent, nodes['SAN'].parent)))  # end part 2
