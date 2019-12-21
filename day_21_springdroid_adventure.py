from collections import defaultdict
import itertools


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


def part_1(data):
    # prog = Intcode(data, None)
    # line = ""
    # for a in prog.run():
    #     if a is None:
    #         prog.values = [ord(c) for c in input()] + [ord("\n")]
    #     else:
    #         try:
    #             v = chr(a)
    #             if v == "\n":
    #                 print(line)
    #                 line = ""
    #             else:
    #                 line += chr(a)
    #         except ValueError:
    #             return

    # (!a|!b|!c)&h
    springscript = ["NOT A J", "NOT B T", "OR T J", "NOT C T", "OR T J",
                    "AND D J", "WALK"]
    values = itertools.chain.from_iterable([ord(c) for c in inst] + [ord("\n")]
                                           for inst in springscript)
    prog = Intcode(data, list(values))
    *_, output = prog.run()
    return output


def part_2(data):
    # (!a|!b|!c)&(e|h)
    springscript = ["NOT A J", "NOT B T", "OR T J", "NOT C T", "OR T J",
                    "AND D J", "NOT H T", "NOT T T", "OR E T", "AND T J",
                    "RUN"]
    values = itertools.chain.from_iterable([ord(c) for c in inst] + [ord("\n")]
                                           for inst in springscript)
    prog = Intcode(data, list(values))
    *_, output = prog.run()
    return output


if __name__ == '__main__':
    with open('day_21_input.txt', 'r') as f:
        inp = f.read()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
