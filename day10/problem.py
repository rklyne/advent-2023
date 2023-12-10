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


Path = list[Tuple[Move, Cell]]


def find_loop(grid: Grid) -> Path:
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
        loop: Path = []
        while True:
            try:
                pos = grid.move(pos, move)
            except KeyError:
                print(f"Can't move {move} from {pos}")
                break
            loop.append((move, pos))
            if pos == start:
                # print(f"a winner: {loop}")
                return loop

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


left_turns: Dict[Move, Move] = {
    LEFT: DOWN,
    DOWN: RIGHT,
    RIGHT: UP,
    UP: LEFT
}
right_turns: Dict[Move, Move] = {v: k for k, v in left_turns.items()}


def turn_left(move: Move) -> Move:
    return left_turns[move]


def turn_right(move: Move) -> Move:
    return right_turns[move]


directions: list[Move] = [UP, DOWN, LEFT, RIGHT]


def expanded_area(grid: Grid, input_cells: list[Cell]) -> Tuple[bool, int]:
    to_check: list[Cell] = input_cells[:]
    inside = set([])
    checks = 0
    while to_check:
        cell = to_check.pop()
        if cell in inside:
            continue
        checks += 1
        if cell[CELL_ITEM] != ".":
            raise RuntimeError(cell)
        inside.add(cell)
        for d in directions:
            try:
                new_cell = grid.move(cell, d)
            except KeyError:
                # This is outside if we can move off the grid from here.
                return False, 0
            if new_cell[CELL_ITEM] == ".":
                to_check.append(new_cell)
    # print(checks, len(cells), len(inside), inside)
    print(f"did {checks} checks over {len(input_cells)} inputs")
    return True, len(inside)


def part2(input: Input):
    grid = Grid(input)
    loop = list(find_loop(grid))
    loop_cells = set(loop)
    coords: set[Pos] = set([
        (cell[CELL_ROW], cell[CELL_COL])
        for (m, cell) in loop
    ])
    new_input = "\n".join([
        item if (row, col) in coords else "."
        for row, line in enumerate(input)
        for col, item in enumerate(line)
    ])
    # grid = Grid(new_input)
    area_l_starts = []
    area_r_starts = []
    for turn in [turn_left, turn_right]:
        for move, cell in loop:
            try:
                l_cell = grid.move(cell, turn_left(move))
            except KeyError:
                continue
            else:
                if l_cell[CELL_ITEM] == ".":
                    area_l_starts.append(l_cell)
            try:
                r_cell = grid.move(cell, turn_right(move))
            except KeyError:
                continue
            else:
                if r_cell[CELL_ITEM] == ".":
                    area_r_starts.append(r_cell)
    answer = -100
    for starts in [
        area_r_starts,
        area_l_starts,
    ]:
        is_inside, size = expanded_area(grid, starts)
        print(f"{is_inside}: {size}")
        if is_inside:
            answer = size
    return answer


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

    def test_part2_square(self):
        square = """
.....
.S-7.
.|.|.
.L-J.
.....
""".strip()
        self.assertEqual(1, part2(parse(square)))

    def test_part2_example_answer1(self):
        square = """
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
""".strip()
        self.assertEqual(4, part2(parse(square)))

    def test_part2_example_answer2(self):
        square = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""".strip()
        self.assertEqual(4, part2(parse(square)))

    def test_part2_example_answer3(self):
        square = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...

""".strip()
        self.assertEqual(8, part2(parse(square)))

    def test_part2_example_answer4(self):
        square = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""".strip()
        self.assertEqual(10, part2(parse(square)))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
