from collections import Counter


def part_1(data):
    w, h = 25, 6
    layers = [data[i:i+w*h] for i in range(0, len(data), w*h)]
    counter = Counter(min(layers, key=lambda x: Counter(x)["0"]))
    return counter["1"] * counter["2"]


def part_2(data):
    w, h = 25, 6
    image = [2] * w * h

    layers = [map(int, data[i:i+w*h]) for i in range(0, len(data), w*h)]
    for layer in layers:
        image = [i if j == 2 else j for i, j in zip(layer, image)]

    image = [[" ", "#", " "][i] for i in image]
    for i in range(0, len(image), w):
        print("".join(image[i:i+w]))


if __name__ == '__main__':
    with open('day_08_input.txt', 'r') as f:
        inp = f.read()
        print("Part 1 answer: " + str(part_1(inp)))
        print("Part 2 answer: ")
        part_2(inp)
