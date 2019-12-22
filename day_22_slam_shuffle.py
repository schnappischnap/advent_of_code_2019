from collections import deque


def part_1(data):
    deck = deque(range(10007))
    for line in data:
        line = line.split()
        if line[-1] == "stack":
            deck.reverse()
        elif line[0] == "cut":
            deck.rotate(-int(line[-1]))
        elif line[0] == "deal":
            new_deck = [0]*10007
            inc = int(line[-1])
            for i in range(len(deck)):
                new_deck[(i*inc) % len(deck)] = deck[i]
            deck = deque(new_deck)
    return deck.index(2019)


def part_2(data):
    # https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju/
    def mod_inv(v):
        return pow(v % card_count, card_count - 2, card_count)

    card_count = 119315717514047
    cycles = 101741582076661

    increment_mul = 1
    offset_dif = 0
    for line in data:
        line = line.split()
        if line[-1] == "stack":
            increment_mul *= -1
            increment_mul %= card_count
            offset_dif += increment_mul
            offset_dif %= card_count
        elif line[0] == "cut":
            offset_dif += increment_mul * int(line[-1])
            offset_dif %= card_count
        elif line[0] == "deal":
            increment_mul *= mod_inv(int(line[-1]))
            increment_mul %= card_count

    increment = pow(increment_mul, cycles, card_count)
    offset = offset_dif * (1-increment) * mod_inv(1-increment_mul)
    offset %= card_count

    return (offset + 2020 * increment) % card_count


if __name__ == '__main__':
    with open('day_22_input.txt', 'r') as f:
        inp = f.readlines()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: " + str(part_2(inp)))
