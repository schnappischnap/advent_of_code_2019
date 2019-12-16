import itertools


def part_1(data):
    data = [int(v) for v in data.strip()]
    repeating_base = [0, 1, 0, -1]

    for _ in range(100):
        new_data = []
        for i in range(len(data)):
            repeating = [a for a in repeating_base for _ in range(i+1)]
            repeating = repeating[1:] + repeating[:1]
            value = sum(v1 * v2 for v1, v2 in zip(data, itertools.cycle(repeating)))
            new_data.append(abs(value) % 10)
        data = new_data

    return "".join(str(v) for v in data[:8])


def part_2(data):
    data = [int(v) for v in data.strip()] * 10000
    offset = int("".join(str(v) for v in data[:7]))
    data = data[offset:]

    for _ in range(100):
        partial_sum = sum(i for i in data)
        for i, v in enumerate(data):
            data[i] = partial_sum % 10
            partial_sum -= v

    return "".join(str(v) for v in data[:8])


if __name__ == '__main__':
    with open('day_16_input.txt', 'r') as f:
        inp = f.read()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
