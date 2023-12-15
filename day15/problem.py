import typing
import unittest

from data import data, example


Input = list[str]


def parse(input: str) -> Input:
    return input.replace("\n", "").split(",")


def hash(s):
    total = 0
    for c in s:
        total = ((total + ord(c)) * 17 ) % 256
    return total

def part1(input: Input):
    return sum(map(hash, input))


def part2(input: Input):
    return 0


class Tests(unittest.TestCase):
    @unittest.skip
    def test_parse(self):
        self.assertEqual("-", parse(example))

    def test_part1_example_answer(self):
        self.assertEqual(1320, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(-1, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(-1, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
