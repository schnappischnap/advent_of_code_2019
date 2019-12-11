from collections import defaultdict


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


def part_1(data):
    paint = defaultdict(int)
    x, y = 0, 0
    dx, dy = 0, -1

    prog = Intcode(data, 0)
    for i, v in enumerate(prog.run()):
        if i % 2 == 0:
            paint[(x, y)] = v
        else:
            if v == 0:
                dx, dy = dy, -dx
            else:
                dx, dy = -dy, dx
            x, y = x+dx, y+dy
            prog.value = paint[(x, y)]

    return len(paint)


def part_2(data):
    paint = defaultdict(int)
    paint[(0, 0)] = 1
    x, y = 0, 0
    dx, dy = 0, -1
    min_x, max_x, min_y, max_y = 0, 0, 0, 0

    prog = Intcode(data, 1)
    for i, v in enumerate(prog.run()):
        if i % 2 == 0:
            paint[(x, y)] = v
        else:
            if v == 0:
                dx, dy = dy, -dx
            else:
                dx, dy = -dy, dx
            x, y = x+dx, y+dy
            prog.value = paint[(x, y)]

            min_x = min(x, min_x)
            max_x = max(x, max_x)
            min_y = min(y, min_y)
            max_y = max(y, max_y)

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            print("#" if paint[(x, y)] == 1 else " ", end="")
        print()


if __name__ == '__main__':
    with open('day_11_input.txt', 'r') as f:
        inp = f.read()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: ")
        part_2(inp)
