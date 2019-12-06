from collections import defaultdict


def part_1(data):
    satellites = defaultdict(list)
    for line in data:
        satellites[line[:3]].append(line[4:7])

    def checksum(obj, level=0):
        if obj not in satellites:
            return level
        return level + sum(checksum(s, level+1) for s in satellites[obj])

    return checksum("COM")


def part_2(data):
    primary = {line[4:7]: line[:3] for line in data}

    def get_path(obj, path):
        return get_path(primary[obj], path+[obj]) if obj in primary else path

    you_path = get_path(primary["YOU"], [])
    san_path = get_path(primary["SAN"], [])
    common = sum(node in san_path for node in you_path)
    return len(you_path) + len(san_path) - (common * 2)


if __name__ == '__main__':
    with open('day_06_input.txt', 'r') as f:
        inp = f.readlines()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
