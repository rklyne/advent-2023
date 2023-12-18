from typing import Literal, Tuple, Iterable
import typing
import unittest

from data import data, example


Colour = str  # "ce122f"
Steps = int
Direction = Literal["L", "R", "U", "D"]
Move = Tuple[Direction, Steps, Colour]
Input = list[Move]
Coord = Tuple[int, int]
Board = list[list[int]]


def parse(input: str) -> Input:
    parsed = []
    for line in input.split("\n"):
        # U 4 (#2d3353)
        d, s, c = line.split(" ")
        parsed.append((d, int(s), c[2:-1]))
    return parsed


def move(pos: Coord, move: Move) -> Coord:
    offset = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1),
    }[move[0]]
    steps = move[1]
    return (
        pos[0] + (steps * offset[0]),
        pos[1] + (steps * offset[1]),
    )


def get_cells(start, end) -> Iterable[Coord]:
    the_range = lambda a, b: range(min(a, b), max(a, b) + 1)
    for i in the_range(start[0], end[0]):
        for ii in the_range(start[1], end[1]):
            yield (i, ii)


directions: list[Direction] = list("UDLR")


def expand_board(board: Board):
    to_check: list[Coord] = []

    for row_num, row in enumerate(board):
        try:
            col = row.index(1)
            if row[col+1] != 1:
                to_check.append((row_num, col+1))
        except ValueError:
            pass

    start_checks = len(to_check)
    checks = 0
    while to_check:
        pos = to_check.pop()
        row, col = pos
        if board[row][col]:
            continue
        checks += 1
        board[row][col] = 1
        for d in directions:
            to_check.append(move(pos, (d, 1, '')))
    print(f"{start_checks}->{checks}")


def part1(input: Input):
    counts = {
        "U": 0,
        "D": 0,
        "L": 0,
        "R": 0,
    }
    for item in input:
        counts[item[0]] += item[1]

    start = counts["U"], counts["L"]
    max_row = counts["U"] + counts["D"]
    max_col = counts["L"] + counts["R"]

    board: Board = [[0] * (max_col + 2) for i in range(max_row + 2)]
    print(f"{max_row}x{max_col}")
    pos = start
    for i in input:
        end = move(pos, i)

        # MARK WALL
        for i, ii in get_cells(pos, end):
            board[i][ii] = 1

        pos = end

    if max_row < 50:
        dprint(board)
    expand_board(board)
    dprint(board)
    return sum(map(sum, board))


def dprint(board: Board):
    transpose = lambda x: list(zip(*x))
    board = [row for row in board if row.count(0) != len(row)]
    board = transpose([row for row in transpose(board) if row.count(0) != len(row)])
    print("\n".join(["".join(map(str, row)) for row in board]))
    print("_" * 5)


def part2(input: Input):
    return 0


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(("R", 6, "70c710"), parse(example)[0])

    def test_part1_example_answer(self):
        self.assertEqual(62, part1(parse(example)))

    # @unittest.skip
    def test_part1_answer(self):
        self.assertEqual(-1, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(-1, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
