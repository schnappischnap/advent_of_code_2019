from collections import deque, defaultdict
import string


def neighbours(x, y):
    return [(x+dx, y+dy) for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]]


def get_path(start, end, vault):
    paths = deque([[start]])
    visited = {start}
    while len(paths):
        path = paths.popleft()
        pos = path[-1]
        if pos == end:
            return path
        for n in neighbours(pos[0], pos[1]):
            if vault.get(n, "#") != "#" and n not in visited:
                visited.add(n)
                paths.append(path+[n])
    return []


def part_1(data):
    key_positions = {c: (x, y)
                     for y, line in enumerate(data)
                     for x, c in enumerate(line)
                     if c in string.ascii_lowercase or c == "@"}
    vault = {(x, y): c
             for y, line in enumerate(data)
             for x, c in enumerate(line)}

    key_to_key = defaultdict(dict)
    for k1, pos1 in key_positions.items():
        for k2, pos2 in key_positions.items():
            if k1 == k2:
                continue
            path = get_path(pos1, pos2, vault)
            doors = []
            keys = []
            for pos in path:
                cell = vault[pos]
                if cell in string.ascii_uppercase and cell.lower() != k1:
                    doors.append(cell.lower())
                elif cell in string.ascii_lowercase:
                    keys.append(cell)
            key_to_key[k1][k2] = (len(path)-1, doors, keys)

    min_steps = 10000000
    queue = deque([("@", ("@",), 0)])
    visited = {("@", ("@",), 0)}
    while len(queue):
        cell, keys, steps = queue.pop()

        if len(keys) == 27:
            min_steps = min(min_steps, steps)
            continue

        for n_cell, (n_steps, doors, n_keys) in key_to_key[cell].items():
            if n_cell in keys:
                continue
            if all(d in keys for d in doors):
                a_keys = tuple(sorted(keys+tuple(k for k in n_keys if k not in keys)))
                if (n_cell, a_keys, steps+n_steps) not in visited:
                    visited.add((n_cell, a_keys, steps+n_steps))
                    queue.append((n_cell, a_keys, steps+n_steps))

    return min_steps


def part_2(data):
    return


if __name__ == '__main__':
    with open('day_18_input.txt', 'r') as f:
        inp = f.readlines()
        # print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
