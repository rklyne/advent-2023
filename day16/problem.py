from typing import Tuple, Dict, Literal
import typing
import unittest

from data import data, example


BoardIn = list[str]
Input = BoardIn

Coord = Tuple[int, int]
Direction = Literal["U", "D", "L", "R"]
Beam = Tuple[Coord, Direction]
Item = Literal[".", "|", "-", "/", "\\"]


def parse(input: str) -> Input:
    return input.split("\n")


def get_tile(board: BoardIn, pos: Coord) -> Item:
    return board[pos[0]][pos[1]]


def inside_board(board: BoardIn, pos: Coord) -> bool:
    row, col = pos
    return row >= 0 and row < len(board) and col >= 0 and col < len(board[0])


def move(pos: Coord, d: Direction) -> Coord:
    row, col = pos
    if d == "U":
        return (row - 1, col)
    if d == "D":
        return (row + 1, col)
    if d == "L":
        return (row, col - 1)
    if d == "R":
        return (row, col + 1)
    return pos


def print_energy(board: BoardIn, energised: set[Coord]):
    grid = [["."] * len(board[0]) for _ in range(len(board))]
    for cell in energised:
        row, col = cell
        grid[row][col] = "#"
    print("\n"+"\n".join([''.join(c for c in line) for line in grid]))


def part1(board: Input):
    return get_energy(board, [((0, 0), "R")])


def get_energy(board: BoardIn, start: list[Beam]):
    energised: set[Coord] = set()
    seen: set[Beam] = set()
    todo: list[Beam] = start[:]
    while todo:
        beam = todo.pop()
        if beam in seen:
            continue
        else:
            seen.add(beam)
        pos, direc = beam
        if not inside_board(board, pos):
            continue
        energised.add(pos)
        tile = get_tile(board, pos)
        if (
            tile == "."
            or (direc in "LR" and tile == "-")
            or (direc in "UD" and tile == "|")
        ):
            next_tile = move(pos, direc)
            todo.append(((next_tile), direc))
        if direc in "LR" and tile == "|":
            todo.append((move(pos, "U"), "U"))
            todo.append((move(pos, "D"), "D"))
        if direc in "UD" and tile == "-":
            todo.append((move(pos, "L"), "L"))
            todo.append((move(pos, "R"), "R"))
        if tile == "/":
            new_dir: Direction = {
                "L": "D",
                "R": "U",
                "U": "R",
                "D": "L",
            }[direc]
            todo.append((move(pos, new_dir), new_dir))
        if tile == "\\":
            new_dir: Direction = {
                "L": "U",
                "U": "L",
                "R": "D",
                "D": "R",
            }[direc]
            todo.append((move(pos, new_dir), new_dir))
    return len(energised)


def part2(board: Input):
    max_row = len(board)
    max_col = len(board[0])
    starts: list[Beam] = []
    for col in range(max_col):
        starts.append(((0, col), "D"))
        starts.append(((max_row, col), "U"))
    for row in range(max_row):
        starts.append(((row, 0), "R"))
        starts.append(((row, max_col), "L"))

    return max([get_energy(board, [start]) for start in starts])


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(r".|...\....", parse(example)[0])

    def test_part1_example_answer(self):
        self.assertEqual(46, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(7111, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(51, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(7831, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
