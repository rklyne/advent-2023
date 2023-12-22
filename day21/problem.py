import typing
import unittest

from data import data, example


Input = list[str]
Board = Input
Coord = tuple[int, int]


def parse(input: str) -> Input:
    return input.split("\n")


def find_rocks(board: Board) -> set[Coord]:
    rocks = set()
    for r, row in enumerate(board):
        for c, tile in enumerate(row):
            if tile == "#":
                rocks.add((r, c))
    return rocks


def find_start(board: Board) -> Coord:
    for r, row in enumerate(board):
        for c, tile in enumerate(row):
            if tile == "S":
                return (r, c)
    raise RuntimeError("no start")


def adjacent(c: Coord) -> list[Coord]:
    return [
        (c[0], c[1] + 1),
        (c[0], c[1] - 1),
        (c[0] + 1, c[1]),
        (c[0] - 1, c[1]),
    ]


def is_on_board(b: Board, c: Coord) -> bool:
    row, col = c
    if row < 0 or row >= len(b):
        return False
    if col < 0 or col >= len(b[0]):
        return False
    return True


def explore(board: Board, locations: set[Coord]) -> set[Coord]:
    rocks = find_rocks(board)
    results: set[Coord] = set()
    for l in locations:
        for new_l in adjacent(l):
            if is_on_board(board, new_l) and new_l not in rocks:
                results.add(new_l)
    return results


def part1(input: Input, steps=64) -> int:
    board = input
    locations: set[Coord] = set([find_start(board)])
    for i in range(steps):
        locations = explore(board, locations)
    return len(locations)


def part2(input: Input):
    return 0


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(".....###.#.", parse(example)[1])

    def test_part1_example_answer(self):
        self.assertEqual(6, part1(parse(example), 3))
        self.assertEqual(16, part1(parse(example), 6))

    def test_part1_answer(self):
        self.assertEqual(-1, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(-1, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
