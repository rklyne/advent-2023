import typing
import unittest

from data import data, example


Input = str


def parse(input: str) -> Input:
    return input


def part1(input: Input):
    return 0


def part2(input: Input):
    return 0


class Tests(unittest.TestCase):
    def test_part1_example_answer(self):
        self.assertEqual(-1, part1(example))

    def test_part1_answer(self):
        self.assertEqual(-1, part1(data))

    def test_part2_example_answer(self):
        self.assertEqual(-1, part2(example))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(data))


if __name__ == "__main__":
    unittest.main()
