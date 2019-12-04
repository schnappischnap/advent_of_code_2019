from collections import Counter


def part_1(data):
    count = 0
    start, stop = map(int, data.split("-"))
    for i in range(start, stop):
        string = str(i)
        if list(string) == sorted(string) and any(v > 1 for v in Counter(string).values()):
            count += 1
    return count


def part_2(data):
    count = 0
    start, stop = map(int, data.split("-"))
    for i in range(start, stop):
        string = str(i)
        if list(string) == sorted(string) and 2 in Counter(string).values():
            count += 1
    return count


if __name__ == '__main__':
    with open('day_04_input.txt', 'r') as f:
        inp = f.read()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
