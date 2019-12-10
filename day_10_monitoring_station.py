import math
from collections import defaultdict
from itertools import zip_longest, chain


def targets_by_direction(p, targets):
    x1, y1 = p

    s_targets = defaultdict(list)
    for target in targets:
        if target == p:
            continue
        x2, y2 = target
        dx, dy = x2-x1, y2-y1
        dist = math.gcd(dx, dy)
        direction = (dx//dist, dy//dist)
        s_targets[direction].append((dist, target))

    for direction in s_targets:
        s_targets[direction] = [t for dist, t in sorted(s_targets[direction])]
    return s_targets


def direction_to_angle(direction):
    return (math.atan2(direction[1], direction[0]) + (math.pi/2)) % (math.pi*2)


def part_1(data):
    asteroids = set((x, y)
                    for y, line in enumerate(data)
                    for x, c in enumerate(line)
                    if c == '#')

    return max(len(targets_by_direction(a, asteroids)) for a in asteroids)


def part_2(data):
    asteroids = set((x, y)
                    for y, line in enumerate(data)
                    for x, c in enumerate(line)
                    if c == '#')

    targets = max((targets_by_direction(a, asteroids) for a in asteroids),
                  key=lambda x: len(x))

    directions = list(targets.keys())
    directions.sort(key=direction_to_angle)
    targets = [targets[direction] for direction in directions]
    target = list(chain.from_iterable(zip_longest(*targets)))[199]

    return (target[0]*100) + (target[1])


if __name__ == '__main__':
    with open('day_10_input.txt', 'r') as f:
        inp = f.readlines()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
