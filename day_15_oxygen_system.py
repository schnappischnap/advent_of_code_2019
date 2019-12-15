from collections import defaultdict, deque


class Intcode:
    def __init__(self, data, value=1):
        self.prog = defaultdict(int)
        for i, j in enumerate(map(int, data.split(","))):
            self.prog[i] = j
        self.value = value
        self.pos = 0
        self.rel_base = 0
        self.output = None

    def set(self, i, v, mode):
        if mode == "0":
            self.prog[self.prog[self.pos+i]] = v
        else:
            self.prog[self.prog[self.pos+i]+self.rel_base] = v

    def get(self, i, mode):
        if mode == "0":
            return self.prog[self.prog[self.pos+i]]
        elif mode == "1":
            return self.prog[self.pos+i]
        elif mode == "2":
            return self.prog[self.prog[self.pos+i]+self.rel_base]

    def run(self):
        while True:
            instruction = str(self.prog[self.pos]).zfill(5)
            opcode = instruction[3:]
            modes = list(reversed(instruction[:3]))

            a, b = None, None
            try:
                a = self.get(1, modes[0])
                b = self.get(2, modes[1])
            except IndexError:
                pass

            if opcode == "01":
                self.set(3, a + b, modes[2])
                self.pos += 4
            elif opcode == "02":
                self.set(3, a * b, modes[2])
                self.pos += 4
            elif opcode == "03":
                self.set(1, self.value, modes[0])
                self.pos += 2
            elif opcode == "04":
                yield self.get(1, modes[0])
                self.output = self.get(1, modes[0])
                self.pos += 2
            elif opcode == "05":
                self.pos = b if a != 0 else self.pos+3
            elif opcode == "06":
                self.pos = b if a == 0 else self.pos+3
            elif opcode == "07":
                self.set(3, 1 if a < b else 0, modes[2])
                self.pos += 4
            elif opcode == "08":
                self.set(3, 1 if a == b else 0, modes[2])
                self.pos += 4
            elif opcode == "09":
                self.rel_base += a
                self.pos += 2
            else:
                assert opcode == "99"
                return self.output


def run(data, part=1):
    dx = {1: 0, 2: 0, 3: -1, 4: 1}
    dy = {1: -1, 2: 1, 3: 0, 4: 0}
    backtrack = {1: 2, 2: 1, 3: 4, 4: 3}

    visited = {(0, 0)}
    path = deque([(0, 0, 0)])
    max_path = 0
    x, y = 0, 0
    prog = Intcode(data)
    prog_iter = iter(prog.run())

    while True:
        for i in range(1, 5):
            new_x, new_y = x + dx[i], y + dy[i]
            if (new_x, new_y) in visited:
                continue

            prog.value = i
            output = next(prog_iter)

            if output > 0:
                x, y = new_x, new_y
                visited.add((x, y))
                path.append((x, y, i))
                if output == 1:
                    break
                if output == 2:
                    if part == 1:
                        return len(path) - 1
                    else:
                        path = deque([(x, y, 0)])
                        visited = {(x, y)}
                        max_path = 0
        else:
            max_path = max(max_path, len(path))

            x, y, i = path.pop()
            if i == 0 and part == 2:
                return max_path - 1

            reverse = backtrack[i]
            prog.value = reverse
            x, y = x + dx[reverse], y + dy[reverse]
            next(prog_iter)


if __name__ == '__main__':
    with open('day_15_input.txt', 'r') as f:
        inp = f.read()
        print("Part 1 answer: " + str(run(inp, part=1)))
        print("Part 2 answer: " + str(run(inp, part=2)))
