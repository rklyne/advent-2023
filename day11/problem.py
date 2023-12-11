import typing
from typing import Tuple
import unittest
import itertools
import math

from data import data, example


Galaxy = Tuple[int, int]  # row, col
Input = list[Galaxy]


def parse(input: str) -> Input:
    galaxies: Input = []
    grid = input.split("\n")
    for row, line in enumerate(grid):
        for col, x in enumerate(line):
            if x == "#":
                galaxies.append((row, col))
    return galaxies


def part1(input: Input, pad_size: int = 1):
    galaxies = input

    def find_empties(i: typing.Iterable[int]) -> set[int]:
        lst = list(i)
        count = max(lst)
        non_empty = set(lst)
        empty = set(range(count+1)).difference(non_empty)
        return empty

    empty_rows, empty_cols = map(find_empties, zip(*galaxies))
    num_rows, num_cols = map(max, zip(*galaxies))

    pad_rows = [0] * (num_rows + 1)
    pad_cols = [0] * (num_cols + 1)
    for pad, empties in [(pad_rows, empty_rows), (pad_cols, empty_cols)]:
        end = len(pad)
        for thing in empties:
            for i in range(thing, end):
                pad[i] += pad_size
    total = 0
    galaxies = [
        (row + pad_rows[row], col + pad_cols[col])
        for (row, col) in galaxies
    ]
    for g1, g2 in itertools.product(galaxies, galaxies):
        if g1 < g2:
            total += distance(g1, g2)
    return total


def distance(p: Galaxy, p2: Galaxy) -> int:
    p1x, p1y = p
    p2x, p2y = p2
    return abs(p1x - p2x) + abs(p1y - p2y)


def part2(input: Input):
    return part1(input, 1000000-1)


class Tests(unittest.TestCase):
    def test_parse(self):
        parsed = parse(example)
        for galaxy in [(0, 3), (2, 0), (8, 7)]:
            self.assertIn(galaxy, parsed)

    def test_part1_example_answer(self):
        self.assertEqual(374, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(9233514, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(1030, part1(parse(example), 9))

    def test_part2_example_answer2(self):
        self.assertEqual(8410, part1(parse(example), 99))

    def test_part2_answer(self):
        self.assertEqual(363293506944, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
