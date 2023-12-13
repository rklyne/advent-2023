from typing import Optional
import typing
import unittest

from data import data, example


Line = str
Board = list[Line]
Input = list[Board]


def parse(input: str) -> Input:
    return [board.split("\n") for board in input.split("\n\n")]


valid_sections = set()


def build_valid_sections_set():
    v = []
    for i in range(1, 50, 2):
        v.insert(0, i)
        valid_sections.add(tuple(v))


build_valid_sections_set()


def is_mirrored(board: Board, reflect: int):

    lines_1 = board[:reflect]
    lines_2 = board[reflect:]

    pairs = list(zip(reversed(lines_1), lines_2))
    is_it = all(l == r for l, r in pairs)
    if is_it and False:
        print(is_it, pairs, reflect, board)
    return is_it


def is_nearly_mirrored(board: Board, reflect: int):

    lines_1 = board[:reflect]
    lines_2 = board[reflect:]

    pairs = list(zip(reversed(lines_1), lines_2))
    mismatches = sum(1 if l != r else 0 for line1, line2 in pairs for l, r in zip(line1, line2))
    return mismatches == 1


def find_reflection1(board: Board, is_mirrored=is_mirrored):
    def find(line: str, start: int) -> Optional[int]:
        try:
            return board.index(line, start + 1) - start
        except ValueError:
            return None

    MAX = len(board)
    options = []
    for possible in range(1, MAX):
        reflect_line = possible
        match_length = min(reflect_line, MAX - reflect_line)
        if is_mirrored(board, reflect_line):
            options.append((match_length, reflect_line))
    options = sorted(options)
    if options:
        # print(f"opts: {options}")
        return sorted(options)[-1][1]


def find_reflection2(board):
    return find_reflection1(board, is_nearly_mirrored)


def transpose_board(board: Board) -> Board:
    return ["".join(line) for line in zip(*board)]


def part1(boards: Input):
    horiz = list(map(find_reflection1, boards))
    transposed_boards = list(map(transpose_board, boards))
    vert = list(map(find_reflection1, transposed_boards))
    return (100 * sum(filter(bool, horiz))) + sum(filter(bool, vert))


def part2(boards: Input):
    horiz = list(map(find_reflection2, boards))
    transposed_boards = list(map(transpose_board, boards))
    vert = list(map(find_reflection2, transposed_boards))
    return (100 * sum(filter(bool, horiz))) + sum(filter(bool, vert))


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual("#.##..##.", parse(example)[0][0])

    def test_part1_example_answer_board1(self):
        self.assertEqual(5, part1(parse(example)[:1]))

    def test_part1_example_answer_board2(self):
        self.assertEqual(400, part1(parse(example)[1:2]))

    def test_puzzle_board_1(self):
        board = """
##.#........#.#
###.##.##.##.##
..####.##.####.
....##....##...
####........###
##..###..###..#
...#..####..#..
.#....#..#....#
..#..#.##.#..#.
###.#......#.##
......####.....
""".strip()
        parsed = parse(board)
        self.assertEqual(8, part1(parsed))
        self.assertEqual(800, part1(map(transpose_board, parsed)))

    def test_puzzle_board_2(self):
        board = """
###.##.##.##.##
..####.##.####.
...............
""".strip()
        parsed = parse(board)
        self.assertEqual(8, part1(parsed))
        self.assertEqual(800, part1(map(transpose_board, parsed)))

    def test_puzzle_board_3(self):
        board = """
#......##....
#######..####
..#.##.##.##.
###.##....##.
..#.##....##.
#.#.##....##.
##.####..####
.#.#........#
##.##########
""".strip()
        parsed = parse(board)
        # new = [''.join(reversed(line)) for line in parsed[0]]
        self.assertEqual(8, part1(parsed))
        self.assertEqual(800, part1(map(transpose_board, parsed)))

    def test_puzzle_board_4(self):
        board = """
..##...####..
##.###..##..#
..#..##.#####
..#.#########
...#.#.#..#.#
...##..#..#..
....##.####.#
..#.##.#..#.#
...##########
..##.###..###
####.#..##..#
""".strip()
        parsed = parse(board)
        # new = [''.join(reversed(line)) for line in parsed[0]]
        self.assertEqual(1, part1(parsed))
        self.assertEqual(100, part1(map(transpose_board, parsed)))

    def test_part1_example_answer(self):
        self.assertEqual(405, part1(parse(example)))

    def test_part1_answer(self):
        # 3238 too low
        # 25668 too low
        # 32139 too low
        # 33155 wrong
        self.assertEqual(33780, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(400, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(23479, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
