from collections import defaultdict


class Intcode:
    def __init__(self, data, values=None):
        self.prog = defaultdict(int)
        for i, j in enumerate(map(int, data.split(","))):
            self.prog[i] = j
        if values is None:
            self.values = []
        else:
            self.values = values
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
                if len(self.values) == 0:
                    yield None
                self.set(1, self.values.pop(0), modes[0])
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


def neighbours(x, y):
    return [(x+dx, y+dy) for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]]


def part_1(data):
    prog = Intcode(data)
    string = "".join(chr(a) for a in prog.run())
    view = [[a for a in line] for line in string.split()]

    answer = sum(x * y
                 for y, line in enumerate(view)
                 for x, v in enumerate(line)
                 if v == "#" and 0 < x < len(line)-1 and 0 < y < len(view)-1
                 and all(view[y2][x2] == "#" for x2, y2 in neighbours(x, y)))

    return answer


def part_2(data):
    # prog = Intcode(data, None)
    # prog.prog[0] = 2
    #
    # line = ""
    # for a in prog.run():
    #     if a is None:
    #         prog.values = [ord(c) for c in input()] + [ord("\n")]
    #     elif chr(a) == "\n":
    #         print(line)
    #         line = ""
    #     elif a < 256:
    #         line += chr(a)
    #     else:
    #         return a

    main = "A,B,A,C,B,C,A,C,B,C\n"
    a = "L,8,R,10,L,10\n"
    b = "R,10,L,8,L,8,L,10\n"
    c = "L,4,L,6,L,8,L,8\n"
    values = [ord(c) for c in main+a+b+c] + [ord("n")] + [ord("\n")]
    prog = Intcode(data, values)
    prog.prog[0] = 2
    *_, output = prog.run()
    return output


if __name__ == '__main__':
    with open('day_17_input.txt', 'r') as f:
        inp = f.read()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
