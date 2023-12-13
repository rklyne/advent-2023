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
    return all(
        l == r
        for l, r in zip(reversed(line[:reflect]), line[reflect])
        for line in board
    )

def find_reflection(board: Board):
    def find(line: str, start: int) -> Optional[int]:
        try:
            return board.index(line, start + 1) - start
        except ValueError:
            return None

    matching_lines = [find(line, idx) for idx, line in enumerate(board)]
    options = []
    for possible in [idx for idx, n in enumerate(matching_lines) if n == 1]:
        reflect_line = possible + 1
        # TODO: something goes wrong with finding the match section
        match_length = min(reflect_line, len(matching_lines) - reflect_line)
        match_start = reflect_line - match_length
        if reflect_line < match_length:
            match_start = 0
        match_section = matching_lines[match_start : reflect_line]
        is_contiguous = tuple(match_section) in valid_sections
        print((reflect_line, len(match_section), match_length), matching_lines, match_section)
        if is_contiguous:
            options.append((match_length, reflect_line))
    options = sorted(options)
    if options:
        print(f"opts: {options}")
        return sorted(options)[-1][1]


def transpose_board(board: Board) -> Board:
    return ["".join(line) for line in zip(*board)]


def part1(boards: Input):
    horiz = list(map(find_reflection, boards))
    transposed_boards = list(map(transpose_board, boards))
    vert = list(map(find_reflection, transposed_boards))
    pairs = list(zip(*(horiz, vert)))
    for i, (h, v) in enumerate(pairs):
        if h is None and v is None:
            print(i)
            print("****")
            print("\n".join(boards[i]))
            print("****")
            print("\n".join(transposed_boards[i]))
            print("****")
    print(f"x: {pairs}")
    return (100 * sum(filter(bool, horiz))) + sum(filter(bool, vert))


def part2(input: Input):
    return 0


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
        # new = [''.join(reversed(line)) for line in parsed[0]]
        self.assertEqual(8, part1(parsed))

    def test_puzzle_board_2(self):
        board = """
###.##.##.##.##
..####.##.####.
...............
""".strip()
        parsed = parse(board)
        # new = [''.join(reversed(line)) for line in parsed[0]]
        self.assertEqual(1, part1(parsed))

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
        self.assertEqual(800, part1(parsed))

    def test_part1_example_answer(self):
        self.assertEqual(405, part1(parse(example)))

    def test_part1_answer(self):
        # 3238 too low
        # 25668 too low
        # 32139 too low
        # 33155 wrong
        self.assertEqual(-1, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(-1, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
