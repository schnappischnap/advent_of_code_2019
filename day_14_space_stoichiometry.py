from collections import defaultdict
import math
import re


def get_ore(reactions, target, target_amount, surpluses=None):
    if target == "ORE":
        return target_amount

    if surpluses is None:
        surpluses = defaultdict(int)

    if target_amount <= surpluses[target]:
        surpluses[target] -= target_amount
        return 0

    target_amount -= surpluses[target]
    surpluses[target] = 0

    out_qty, reactants = reactions[target]
    cycles = math.ceil(target_amount/out_qty)

    ore = 0
    for in_qty, reactant in reactants:
        in_qty *= cycles
        ore += get_ore(reactions, reactant, in_qty, surpluses)
    surpluses[target] += out_qty * cycles - target_amount
    return ore


def part_1(data):
    reactions = {}
    for line in data:
        qty = re.findall(r"(\d+)", line)
        mat = re.findall(r"([^\d\W]+)", line)
        reactions[mat[-1]] = (int(qty[-1]), [(int(i), s) for i, s in zip(qty[:-1], mat[:-1])])

    return get_ore(reactions, "FUEL", 1)


def part_2(data):
    reactions = {}
    for line in data:
        qty = re.findall(r"(\d+)", line)
        mat = re.findall(r"([^\d\W]+)", line)
        reactions[mat[-1]] = (int(qty[-1]), [(int(i), s) for i, s in zip(qty[:-1], mat[:-1])])

    low, high = 0, 10000000
    while low < high:
        fuel = (low + high) // 2
        ore = get_ore(reactions, "FUEL", fuel)
        if ore < 1000000000000:
            low = fuel
        if ore > 1000000000000:
            high = fuel - 1 

    return low


if __name__ == '__main__':
    with open('day_14_input.txt', 'r') as f:
        inp = f.readlines()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
