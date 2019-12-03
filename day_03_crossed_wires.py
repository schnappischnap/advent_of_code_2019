def get_path(path):
    steps = dict()
    pos = (0, 0)
    step_count = 0
    for instruction in path.split(","):
        delta = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}[instruction[0]]
        for _ in range(int(instruction[1:])):
            step_count += 1
            pos = (pos[0]+delta[0], pos[1]+delta[1])
            if pos not in steps:
                steps[pos] = step_count
    return steps


def part_1(data):
    intersections = set(get_path(data[0]).keys() & get_path(data[1]).keys())
    return min(abs(t[0])+abs(t[1]) for t in intersections)


def part_2(data):
    a_steps = get_path(data[0])
    b_steps = get_path(data[1])
    intersections = set(a_steps.keys() & b_steps.keys())
    return min(a_steps[t]+b_steps[t] for t in intersections)


if __name__ == '__main__':
    with open('day_03_input.txt', 'r') as f:
        inp = f.readlines()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
