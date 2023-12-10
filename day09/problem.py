import unittest

from data import data, example


History = list[int]
Input = list[History]


def parse(input: str) -> Input:
    return [[int(i) for i in line.split(" ")] for line in input.split("\n")]


def next_value(history: History) -> int:
    stack = []
    line = history
    while set(line) != set([0]):
        stack.append(line[-1])
        line = [y - x for (x, y) in zip(line, line[1:])]
    return sum(stack)


def part1(input: Input):
    return sum(map(next_value, input))


def part2(input: Input):
    return sum(map(next_value, [list(reversed(line)) for line in input]))


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual([0, 3, 6, 9, 12, 15], parse(example)[0])

    def test_part1_example_answer(self):
        self.assertEqual(114, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(1806615041, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(2, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(1211, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
