from collections import defaultdict, deque
import string


def get_neighbours(x, y):
    return [(x+dx, y+dy) for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]]


def part_1(data):
    grid = [[c for c in line.rstrip()] for line in data]
    traversable = [(x, y)
                   for y, line in enumerate(grid)
                   for x, c in enumerate(line)
                   if c == "."]
    portals = {}
    neighbours = defaultdict(list)

    for x, y in traversable:
        for nx, ny in get_neighbours(x, y):
            if grid[ny][nx] == ".":
                neighbours[(x, y)].append((nx, ny))
            elif grid[ny][nx] in string.ascii_uppercase:
                if ny == y-1:
                    portal_id = grid[y-2][x]+grid[y-1][x]
                elif ny == y+1:
                    portal_id = grid[y+1][x]+grid[y+2][x]
                elif nx == x-1:
                    portal_id = grid[y][x-2]+grid[y][x-1]
                else:
                    portal_id = grid[y][x+1]+grid[y][x+2]

                if portal_id in portals:
                    neighbours[(x, y)].append(portals[portal_id])
                    neighbours[portals[portal_id]].append((x, y))
                else:
                    portals[portal_id] = (x, y)

    def get_path(start, end):
        paths = deque([[start]])
        visited = {start}
        while len(paths):
            path = paths.popleft()
            coord = path[-1]
            if coord == end:
                return path
            for n in neighbours[coord]:
                if n not in visited:
                    visited.add(n)
                    paths.append(path + [n])
        return []

    return len(get_path(portals["AA"], portals["ZZ"])) - 1


def part_2(data):
    grid = [[c for c in line.rstrip()] for line in data]
    traversable = [(x, y)
                   for y, line in enumerate(grid)
                   for x, c in enumerate(line)
                   if c == "."]
    portals = {}
    neighbours = defaultdict(list)
    max_x = len(grid[2])-1
    max_y = len(grid)-3

    for x, y in traversable:
        for nx, ny in get_neighbours(x, y):
            if grid[ny][nx] == ".":
                neighbours[(x, y)].append(((nx, ny), 0))
            elif grid[ny][nx] in string.ascii_uppercase:
                if ny == y - 1:
                    portal_id = grid[y - 2][x] + grid[y - 1][x]
                elif ny == y + 1:
                    portal_id = grid[y + 1][x] + grid[y + 2][x]
                elif nx == x - 1:
                    portal_id = grid[y][x - 2] + grid[y][x - 1]
                else:
                    portal_id = grid[y][x + 1] + grid[y][x + 2]

                level_change = -1 if x == 2 or x == max_x or y == 2 or y == max_y else 1

                if portal_id in portals:
                    neighbours[(x, y)].append((portals[portal_id], level_change))
                    neighbours[portals[portal_id]].append(((x, y), -level_change))
                else:
                    portals[portal_id] = (x, y)

    def get_path(start, end):
        paths = deque([[(start, 0)]])
        visited = {(start, 0)}
        while len(paths):
            path = paths.popleft()
            coord, level = path[-1]
            if coord == end and level == 0:
                return path
            for n, lc in neighbours[coord]:
                if level == 0 and lc == -1:
                    continue
                state = (n, level+lc)
                if state not in visited:
                    visited.add(state)
                    paths.append(path+[state])
        return []

    return len(get_path(portals["AA"], portals["ZZ"])) - 1


if __name__ == '__main__':
    with open('day_20_input.txt', 'r') as f:
        inp = f.readlines()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
