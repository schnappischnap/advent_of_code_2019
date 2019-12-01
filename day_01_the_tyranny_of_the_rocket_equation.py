def part_1(data):
    return sum(int(line)//3 - 2 for line in data)


def part_2(data):
    total = 0
    for line in data:
        fuel = int(line)//3 - 2
        while fuel > 0:
            total += fuel
            fuel = fuel//3 - 2
    return total


if __name__ == '__main__':
    with open('day_01_input.txt', 'r') as f:
        inp = f.readlines()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
