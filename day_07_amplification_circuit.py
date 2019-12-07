import itertools


class Intcode:
    def __init__(self, data, phase):
        self.prog = list(map(int, data.split(",")))
        self.phase = phase
        self.pos = 0
        self.used_phase = False
        self.output = None

    def run(self, signal):
        while True:
            instruction = str(self.prog[self.pos]).zfill(5)
            opcode = instruction[3:]
            c_mode, b_mode, a_mode = instruction[:3]

            a, b = None, None
            try:
                a = self.prog[self.pos+1] if a_mode == "1" else self.prog[self.prog[self.pos+1]]
                b = self.prog[self.pos+2] if b_mode == "1" else self.prog[self.prog[self.pos+2]]
            except IndexError:
                pass

            if opcode == "01":
                self.prog[self.prog[self.pos+3]] = a + b
                self.pos += 4
            elif opcode == "02":
                self.prog[self.prog[self.pos+3]] = a * b
                self.pos += 4
            elif opcode == "03":
                self.prog[self.prog[self.pos+1]] = self.phase if not self.used_phase else signal
                self.used_phase = True
                self.pos += 2
            elif opcode == "04":
                self.output = a
                self.pos += 2
                return self.output, False
            elif opcode == "05":
                self.pos = b if a != 0 else self.pos + 3
            elif opcode == "06":
                self.pos = b if a == 0 else self.pos + 3
            elif opcode == "07":
                self.prog[self.prog[self.pos+3]] = 1 if a < b else 0
                self.pos += 4
            elif opcode == "08":
                self.prog[self.prog[self.pos+3]] = 1 if a == b else 0
                self.pos += 4
            elif opcode == "99":
                return self.output, True


def part_1(data):
    biggest = 0
    for permutation in itertools.permutations([0, 1, 2, 3, 4], 5):
        signal = 0
        for prog in [Intcode(data, phase) for phase in permutation]:
            signal = prog.run(signal)[0]
        biggest = max(biggest, signal)

    return biggest


def part_2(data):
    biggest = 0
    for permutation in itertools.permutations([5, 6, 7, 8, 9], 5):
        progs = [Intcode(data, phase) for phase in permutation]
        signal = 0
        while True:
            for i, prog in enumerate(progs):
                signal, completed = prog.run(signal)
                if completed and i == 4:
                    biggest = max(biggest, signal)
                    break
            else:
                continue
            break

    return biggest


if __name__ == '__main__':
    with open('day_07_input.txt', 'r') as f:
        inp = f.read()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
