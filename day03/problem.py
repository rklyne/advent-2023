import typing
import unittest
import re

from data import data, example


Input = list[str]
Span = [int, [int, int]]


def parse(input: str) -> Input:
    lines = ['.' + l + '.' for l in input.split("\n")]
    blank = "." * len(lines[0])
    return [blank] + lines + [blank]


digit = re.compile("[0-9]+")


def part1(input: Input):
    numbers: list[Span] = []
    for y, line in enumerate(input):
        upto = 0
        while True:
            match = digit.search(line, pos=upto)
            if not match:
                break
            start = match.span()[0]
            end = match.span()[1]
            numbers.append((y, (start, end)))
            upto = end
    strings: list[str] = []
    for n in numbers:
        line = n[0]
        start = n[1][0]
        end = n[1][1]
        string = input[line][start:end]
        string_adjacent = ''.join([
            input[line-1][start-1:end+1],
            input[line+1][start-1:end+1],
            input[line][start-1:start],
            input[line][end:end+1],
        ])
        if string_adjacent.count(".") != len(string_adjacent):
            strings.append(string)
    return sum(int(s) for s in strings)


def part2(input: Input):
    return 0


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(".467..114...", parse(example)[1])

    def test_part1_example_answer(self):
        self.assertEqual(4361, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(514969, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(-1, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
