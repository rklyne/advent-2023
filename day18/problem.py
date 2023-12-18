from typing import Literal, Tuple, Iterable
from pprint import pprint
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
            if row[col + 1] != 1:
                to_check.append((row_num, col + 1))
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
            to_check.append(move(pos, (d, 1, "")))
    # print(f"{start_checks}->{checks}")


def part1(input: Input):
    return algo2(input)


def algo1(input: Input):
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
    # print(f"{max_row}x{max_col}")
    pos = start
    for i in input:
        end = move(pos, i)

        # MARK WALL
        for i, ii in get_cells(pos, end):
            board[i][ii] = 1

        pos = end

    expand_board(board)
    # dprint(board)
    return sum(map(sum, board))


def dprint(board: Board):
    transpose = lambda x: list(zip(*x))
    board = [row for row in board if row.count(0) != len(row)]
    board = transpose([row for row in transpose(board) if row.count(0) != len(row)])
    print("\n".join(["".join(map(str, row)) for row in board]))
    print("_" * 5)


first = lambda tpl: tpl[0]
second = lambda tpl: tpl[1]


def colour_instr(c):
    dmap = {
        "0": "R",
        "1": "D",
        "2": "L",
        "3": "U",
    }
    return (dmap[c[5]], int(c[:5], 16), "")


def get_size(box):
    tl, br = box
    return abs((br[0] - tl[0] + 1) * (br[1] - tl[1] + 1))


def part2(input: Input):
    input = [colour_instr(c) for _, _, c in input]
    return algo2(input)


def algo2(input: Input):
    pos: Coord = (0, 0)
    line = [pos]
    for i in input:
        pos = move(pos, i)
        line.append(pos)

    edges: list[Coord] = list(zip(line, line[1:]))
    # print(f"line ... {list(zip(*line[:8]))}")
    # print(f"line debug... {len(list(zip(*line)))}")
    pairs = list(zip(*line))
    rows, cols = [list(sorted(set(xs))) for xs in pairs]
    mins = rows[0], cols[0]
    maxs = rows[-1], cols[-1]
    # print(f"SORTED {rows[:5]} {cols[:5]}")
    # print(f"SCALE {mins} {maxs} (*> {maxs[0] * maxs[1]})")
    squares = [
        (
            (row_span[0], col_span[0]),
            (row_span[1] - 1, col_span[1] - 1),
        )
        # TODO: maybe these need a swap?
        for row_span in zip(rows, rows[1:])
        for col_span in zip(cols, cols[1:])
    ]
    # print(f"reduced GRID: {len(rows)}x{len(cols)} -> {len(squares)}")
    # print(squares[:5])
    # print(f"smallest square {min(map(lambda s: s[1][0] - s[0][0], squares))}x{min(map(lambda s: s[1][1] - s[0][1], squares))}")
    # print(f"largest square {max(map(lambda s: s[1][0] - s[0][0], squares))}x{max(map(lambda s: s[1][1] - s[0][1], squares))}")

    total = 0
    total_size = 0
    included_squares = 0
    square_sizes = []
    for square in squares:
        tl, br = square
        square_size = get_size(square)
        square_sizes.append(square_size)
        point = tl[0] + 1, tl[1] + 1
        # count edges to the left
        crossed_edges = 0
        for edge in edges:
            edge_tl, edge_br = sorted(edge)
            # skip if horizontal:
            if edge_tl[0] == edge_br[0]:
                continue
            assert edge_tl[1] == edge_br[1]
            # if left
            if point[1] < edge_br[1]:
                # if within vertical range
                if point[0] < edge_br[0] and point[0] >= edge_tl[0]:
                    crossed_edges += 1
                    # print(f"crossed {point[0]} ({edge_tl[0]}, {edge_br[0]})")

        if crossed_edges % 2 == 1:
            total += square_size
            included_squares += 1
        total_size += square_size
    # print(f"enclosed_size of {included_squares} squares: {total} / {total_size}")
    # missing = 952408144115 - total
    # print(f"misssing {missing} -> {[s for s in square_sizes if s <= missing]}")
    edge_len = sum(map(get_size, edges))
    edge_len2 = (edge_len - len(edges)) // 2
    print(f"edges ({len(input)}.. {total}) len: {edge_len} {len(edges)}")
    height = maxs[0] - mins[0]
    width = maxs[1] - mins[1]
    pprint(
        {
            "total": total,
            "instructions": len(input),
            "edge count": len(edges),
            "edge_total_length": edge_len,
            "edge adjusted lengt": edge_len2,
            "mins": mins,
            "maxs": maxs,
            "board_size": (height, width),
        }
    )
    return total


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(("R", 6, "70c710"), parse(example)[0])

    def test_parse_colour(self):
        self.assertEqual(("R", 461937, ""), colour_instr("70c710"))
        self.assertEqual(("D", 56407, ""), colour_instr("0dc571"))
        self.assertEqual(("L", 577262, ""), colour_instr("8ceee2"))
        self.assertEqual(("U", 829975, ""), colour_instr("caa173"))

    def test_get_size(self):
        self.assertNumEqual(1, get_size(((0, 0), (0, 0))))
        self.assertNumEqual(4, get_size(((0, 0), (1, 1))))
        self.assertNumEqual(6, get_size(((0, 0), (0, 5))))

    def assertNumEqual(self, x, y):
        self.assertEqual(x, y, f"{x} != {y} ({y-x})")

    def test_part1_example_answer(self):
        self.assertNumEqual(62, part1(parse(example)))

    # @unittest.skip
    def test_part1_answer(self):
        self.assertNumEqual(39_039, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertNumEqual(952_408_144_115, part2(parse(example)))

    @unittest.skip
    def test_part2_answer(self):
        # too low 44644464596913
        self.assertNumEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
