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
        self.input_dry = values is not None

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

    def tick(self):
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
            if len(self.values):
                self.set(1, self.values.pop(0), modes[0])
            else:
                self.set(1, -1, modes[0])
                self.input_dry = True
            self.pos += 2
        elif opcode == "04":
            self.output = self.get(1, modes[0])
            self.pos += 2
            return self.output
        elif opcode == "05":
            self.pos = b if a != 0 else self.pos + 3
        elif opcode == "06":
            self.pos = b if a == 0 else self.pos + 3
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
        if self.input_dry and len(self.values):
            self.input_dry = False
        return None

    def run(self):
        while True:
            yield from self.tick()


def part_1(data):
    progs = [Intcode(data, [i]) for i in range(50)]
    outputs = [[] for _ in range(50)]
    while True:
        for i, prog in enumerate(progs):
            out = prog.tick()
            if out is None:
                continue
            outputs[i].append(out)
            if len(outputs[i]) == 3:
                j, x, y = outputs[i]
                if j == 255:
                    return y
                progs[j].values.extend([x, y])
                outputs[i] = []


def part_2(data):
    prev_y = None
    nat = []
    progs = [Intcode(data, [i]) for i in range(50)]
    outputs = [[] for _ in range(50)]
    while True:
        idle_count = 0
        for i, prog in enumerate(progs):
            out = prog.tick()
            if out is None:
                if prog.input_dry:
                    idle_count += 1
                continue
            outputs[i].append(out)
            if len(outputs[i]) == 3:
                j, x, y = outputs[i]
                if j == 255:
                    nat = [x, y]
                else:
                    progs[j].values.extend([x, y])
                outputs[i] = []
        if idle_count == 50 and len(nat):
            y = nat[1]
            if y == prev_y:
                return y
            prev_y = y
            progs[0].values = [nat[0], nat[1]]


if __name__ == '__main__':
    with open('day_23_input.txt', 'r') as f:
        inp = f.read()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
