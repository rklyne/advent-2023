from typing import Literal, Union, Iterable, Dict, Tuple
import typing
import unittest

from data import data, example


Start = Literal["S"]
Ground = Literal["."]
Pipe = Literal["|", "-", "L", "J", "7", "F"]
Item = Union[Pipe, Start, Ground]
RowT = list[Item]
GridT = list[RowT]
Input = GridT

RowN = int
ColN = int
Pos = typing.Tuple[RowN, ColN]
Cell = typing.Tuple[RowN, ColN, Item]
CELL_ROW = 0
CELL_COL = 1
CELL_ITEM = 2
Offset = Literal[-1, 0, 1]
Move = typing.Tuple[Offset, Offset]


def rows(g: GridT) -> Iterable[int]:
    return range(len(g))


def cols(g: GridT) -> Iterable[int]:
    return range(len(g[0]))


def parse(input: str) -> Input:
    return [[c for c in row] for row in input.split("\n")]


UP: Move = (-1, 0)
DOWN: Move = (1, 0)
LEFT: Move = (0, -1)
RIGHT: Move = (0, 1)


class Grid:
    _cells: typing.Dict[Pos, Cell]
    _directions: Dict[Item, Iterable[Move]] = {
        "-": [RIGHT, LEFT],
        "|": [UP, DOWN],
        "F": [RIGHT, DOWN],
        "7": [LEFT, DOWN],
        "J": [LEFT, UP],
        "L": [RIGHT, UP],
        "S": [RIGHT, DOWN, UP, LEFT],
        ".": [],
    }

    def __init__(self, g: GridT):
        self._cells = {
            (row, col): self._make_cell(row, col, g[row][col])
            for row in rows(g)
            for col in cols(g)
        }

    def _make_cell(self, r: int, c: int, i: Item) -> Cell:
        return r, c, i

    def get_cell(self, r: int, c: int) -> Cell:
        return self._cells[r, c]

    def move(self, cell: Cell, m: Move):
        offrow, offcol = m
        return self.get_cell(
            cell[CELL_ROW] + offrow,
            cell[CELL_COL] + offcol,
        )

    def possible_moves(self, cell: Cell) -> list[Move]:
        return self._directions[cell[CELL_ITEM]]

    def connected_cells(self, cell: Cell) -> list[Tuple[Move, Cell]]:
        cells: list[Tuple[Move, Cell]] = []
        for direction in self.possible_moves(cell):
            cells.append((direction, self.move(cell, direction)))
        return cells

    def iter_cells(self) -> Iterable[Cell]:
        return self._cells.values()

    def get_start(self) -> Cell:
        for c in self.iter_cells():
            if c[CELL_ITEM] == "S":
                return c
        raise RuntimeError("start not found")


def inverse_direction(m: Move) -> Move:
    return {
        UP: DOWN, DOWN: UP,
        LEFT: RIGHT, RIGHT: LEFT
    }[m]


def find_loop(grid: Grid) -> Iterable[Cell]:
    start = grid.get_start()
    directions: list[Move] = [
        UP,
        LEFT,
        DOWN,
        RIGHT,
    ]
    for direction in directions:
        pos = start
        move = direction
        loop: list[Cell] = [start]
        while True:
            try:
                pos = grid.move(pos, move)
            except KeyError:
                print(f"Can't move {move} from {pos}")
                break
            if pos == start:
                # print(f"a winner: {loop}")
                return loop
            loop.append(pos)

            reverse = inverse_direction(move)
            options = grid.possible_moves(pos)
            next_moves = [m for m in options if m != reverse]
            if len(next_moves) != 1:
                # print(f"bad start {direction} ended at {pos} (from {reverse}) after {len(loop)}: {loop} - {next_moves}")
                break
            move = next_moves[0]
    raise RuntimeError("nothing found")


def part1(input: Input):
    grid = Grid(input)
    loop = find_loop(grid)
    return len(loop) // 2


def part2(input: Input):
    return 0


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(["-", "L", "|", "F", "7"], parse(example)[0])

    def test_part1_square(self):
        square = """
.....
.S-7.
.|.|.
.L-J.
.....
""".strip()
        self.assertEqual(4, part1(parse(square)))

    def test_part1_example_answer(self):
        self.assertEqual(4, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(6875, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(-1, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
