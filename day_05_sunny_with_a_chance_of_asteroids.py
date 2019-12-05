def run(data, value=1):
    prog = list(map(int, data.split(",")))

    pos = 0
    while True:
        instruction = str(prog[pos]).zfill(5)
        opcode = instruction[3:]
        c_mode, b_mode, a_mode = instruction[:3]

        a, b = None, None
        try:
            a = prog[pos+1] if a_mode == "1" else prog[prog[pos+1]]
            b = prog[pos+2] if b_mode == "1" else prog[prog[pos+2]]
        except IndexError:
            pass

        if opcode == "01":
            prog[prog[pos+3]] = a + b
            pos += 4
        elif opcode == "02":
            prog[prog[pos+3]] = a * b
            pos += 4
        elif opcode == "03":
            prog[prog[pos+1]] = value
            pos += 2
        elif opcode == "04":
            print(a)
            pos += 2
        elif opcode == "05":
            pos = b if a != 0 else pos + 3
        elif opcode == "06":
            pos = b if a == 0 else pos + 3
        elif opcode == "07":
            prog[prog[pos+3]] = 1 if a < b else 0
            pos += 4
        elif opcode == "08":
            prog[prog[pos+3]] = 1 if a == b else 0
            pos += 4
        elif opcode == "99":
            return


if __name__ == '__main__':
    with open('day_05_input.txt', 'r') as f:
        inp = f.read()
        print("Part 1 answer: ")
        run(inp, 1)
        print("Part 2 answer: ")
        run(inp, 5)
