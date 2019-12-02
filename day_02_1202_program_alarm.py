def part_1(data, noun=12, verb=2):
    prog = list(map(int, data.split(",")))
    prog[1] = noun
    prog[2] = verb

    pos = 0
    while True:
        if prog[pos] == 1:
            prog[prog[pos+3]] = prog[prog[pos+1]] + prog[prog[pos+2]]
        elif prog[pos] == 2:
            prog[prog[pos+3]] = prog[prog[pos+1]] * prog[prog[pos+2]]
        elif prog[pos] == 99:
            return prog[0]
        pos += 4


def part_2(data):
    for n in range(100):
        for v in range(100):
            if part_1(data, n, v) == 19690720:
                return 100 * n + v


if __name__ == '__main__':
    with open('day_02_input.txt', 'r') as f:
        inp = f.read()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
