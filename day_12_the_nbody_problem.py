import re
import math


def one_d_repeat(positions):
    velocities = [0, 0, 0, 0]
    original = (tuple(positions), tuple(velocities))
    steps = 0
    while True:
        steps += 1
        for i, pos in enumerate(positions):
            velocities[i] += sum(pos < p for p in positions) - sum(pos > p for p in positions)
        for i, vel in enumerate(velocities):
            positions[i] += vel
        if (tuple(positions), tuple(velocities)) == original:
            return steps


def lcm(a, b):
    return a * b // math.gcd(a, b)


def part_1(data):
    positions = [tuple(map(int, re.findall(r"-?\d+", line))) for line in data]
    velocities = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

    for _ in range(1000):
        for i, (pos, vel) in enumerate(zip(positions, velocities)):
            new_vel = tuple(vel[j] +
                            sum(pos[j] < p[j] for p in positions) -
                            sum(pos[j] > p[j] for p in positions)
                            for j in range(len(pos)))
            velocities[i] = new_vel
        for i, (pos, vel) in enumerate(zip(positions, velocities)):
            new_pos = tuple(pos[j] + vel[j] for j in range(len(pos)))
            positions[i] = new_pos

    return sum(sum(abs(p) for p in pos) * sum(abs(v) for v in vel)
               for pos, vel in zip(positions, velocities))


def part_2(data):
    positions = [tuple(map(int, re.findall(r"-?\d+", line))) for line in data]

    x_steps = one_d_repeat([p[0] for p in positions])
    y_steps = one_d_repeat([p[1] for p in positions])
    z_steps = one_d_repeat([p[2] for p in positions])

    return lcm(x_steps, lcm(y_steps, z_steps))


if __name__ == '__main__':
    with open('day_12_input.txt', 'r') as f:
        inp = f.readlines()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
