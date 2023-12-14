from typing import Tuple, Dict, Iterable, Literal
import typing
import unittest

from data import data, example


Board = list[str]
Input = Board


def parse(input: str) -> Input:
    return input.split("\n")


def transpose_board(board: Board) -> Board:
    return ["".join(line) for line in zip(*board)]


def rotate_right(board: Board) -> Board:
    return list(reversed(transpose_board(board)))


def move_up(board: Board):
    new = []
    for col in board:
        new.append(
            "#".join(["".join(sorted(chunk, reverse=True)) for chunk in col.split("#")])
        )
    return new


def pboard(board: Board):
    print("\n".join(transpose_board(board)))


def board_score(board: Board) -> int:
    total = 0
    for col in board:
        MAX = len(col)
        total += sum([MAX - i for i, tile in enumerate(col) if tile == "O"])
    return total


def part1(input: Input):
    board = transpose_board(input)
    board = move_up(board)
    return board_score(board)


def do_cycle(board: Board) -> Board:
    new = board
    new = move_up(new)
    new = rotate_right(new)
    new = move_up(new)
    new = rotate_right(new)
    new = move_up(new)
    new = rotate_right(new)
    new = move_up(new)
    new = rotate_right(new)
    return new


def part2(input: Input):
    board = transpose_board(input)
    MAX = 1_000_000_000
    boards = []
    for i in range(MAX):
        new = do_cycle(board)
        board = new
        if board in boards:
            break
        boards.append(board)

    # hit a loop, now expand

    loop_length = list(reversed(boards)).index(board) + 1
    loop_start = len(boards) - loop_length + 1
    extra_cycles = (MAX - loop_start) % loop_length
    for i in range(extra_cycles):
        board = do_cycle(board)

    return board_score(board)


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual("O....#....", parse(example)[0])

    def test_part1_example_answer(self):
        self.assertEqual(136, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(108813, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(64, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(104533, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
