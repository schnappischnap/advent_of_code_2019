from copy import deepcopy


def part_1(data):
    def get_neighbours(x, y):
        return [(x+dx, y+dy)
                for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]
                if 0 <= (x + dx) < 5 and 0 <= (y + dy) < 5]

    bugs = set([(x, y)
                for y, line in enumerate(data)
                for x, c in enumerate(line)
                if c == "#"])
    seen = set()

    while tuple(bugs) not in seen:
        seen.add(tuple(bugs))
        nbugs = set()
        for y in range(5):
            for x in range(5):
                adjacent_bugs = sum(v in bugs for v in get_neighbours(x, y))
                if (x, y) in bugs and adjacent_bugs == 1:
                    nbugs.add((x, y))
                elif (x, y) not in bugs and 1 <= adjacent_bugs <= 2:
                    nbugs.add((x, y))
        bugs = deepcopy(nbugs)

    return sum(2**((y*5)+x)
               for y in range(5)
               for x in range(5)
               if (x, y) in bugs)


def part_2(data):
    def get_neighbours(l, x, y):
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x+dx, y+dy
            if nx == -1:
                yield l-1, 1, 2
            elif nx == 5:
                yield l-1, 3, 2
            elif ny == -1:
                yield l-1, 2, 1
            elif ny == 5:
                yield l-1, 2, 3
            elif (nx, ny) == (2, 2):
                for i in range(5):
                    if x == 1:
                        yield l+1, 0, i
                    elif x == 3:
                        yield l+1, 4, i
                    elif y == 1:
                        yield l+1, i, 0
                    elif y == 3:
                        yield l+1, i, 4
            else:
                yield l, nx, ny

    bugs = set([(0, x, y)
                for y, line in enumerate(data)
                for x, c in enumerate(line)
                if c == "#"])

    for _ in range(200):
        nbugs = set()
        min_level = min(a[0] for a in bugs)
        max_level = max(a[0] for a in bugs)

        for level in range(min_level-1, max_level+2):
            for y in range(5):
                for x in range(5):
                    if (x, y) == (2, 2):
                        continue

                    adjacent_bugs = sum(v in bugs for v in get_neighbours(level, x, y))
                    if (level, x, y) in bugs and adjacent_bugs == 1:
                        nbugs.add((level, x, y))
                    elif (level, x, y) not in bugs and 1 <= adjacent_bugs <= 2:
                        nbugs.add((level, x, y))

        bugs = deepcopy(nbugs)

    return len(bugs)


if __name__ == '__main__':
    with open('day_24_input.txt', 'r') as f:
        inp = f.readlines()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
