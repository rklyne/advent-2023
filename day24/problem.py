from typing import NamedTuple, Optional
import typing
from pprint import pprint
import sympy
import unittest

from data import data, example


class Coord(NamedTuple):
    x: int
    y: int
    z: int


Flake = tuple[Coord, Coord]
Input = list[Flake]


def parse(input: str) -> Input:
    def c(s: str) -> Coord:
        p = s.split(", ")
        return Coord(int(p[0]), int(p[1]), int(p[2]))

    def _parse():
        for l in input.split("\n"):
            a, b = l.split(" @ ")
            yield c(a), c(b)

    return list(_parse())


def intersection(f1: Flake, f2: Flake) -> Optional[Coord]:
    denom = (f1[1].x * f2[1].y) - (f1[1].y * f2[1].x)
    if denom == 0:
        return None
    x = (
        +((f1[0].y - f2[0].y) * (f1[1].x * f2[1].x))
        - (f1[0].x * f2[1].x * f1[1].y)
        + (f2[0].x * f1[1].x * f2[1].y)
    ) / denom
    y = (
        ((f2[0].x - f1[0].x) * f1[1].y * f2[1].y)
        + (f1[0].y * f1[1].x * f2[1].y)
        - (f2[0].y * f1[1].y * f2[1].x)
    ) / denom

    return Coord(x, y, 0)


def sign(n: int) -> int:
    if n == 0:
        return 0
    return n / abs(n)


def is_forward(flake: Flake, coord: Coord, include_z=False) -> bool:
    pos, speed = flake
    dx = sign(coord.x - pos.x) == sign(speed.x)
    dy = sign(coord.y - pos.y) == sign(speed.y)
    if include_z:
        dz = sign(coord.z - pos.z) == sign(speed.z)
    else:
        dz = True
    # print(f"{dx} & {dy}: {pos}@{speed} -> {coord}")
    return dx and dy and dz


def part1(input: Input, in_range=(7, 27)):
    # Find x / y intersection points
    count = 0
    for i, flake in enumerate(input):
        for flake2 in input[i:]:
            inter = intersection(flake, flake2)
            if (
                inter
                and inter.x >= in_range[0]
                and inter.x <= in_range[1]
                and inter.y >= in_range[0]
                and inter.y <= in_range[1]
                and is_forward(flake, inter)
                and is_forward(flake2, inter)
            ):
                # print(f"intersection {flake} x {flake2} @ {inter}")
                count += 1
    return count


def part2(input: Input):
    px, py, pz, vx, vy, vz = sympy.symbols("px, py, pz, vx, vy, vz", real=True)
    eqs = []
    syms = [px, py, pz, vx, vy, vz]
    for i, (pos, vec) in enumerate(input[:5], 1):
        time = sympy.symbols(f"ta{i}", real=True)
        syms.append(time)
        eqs += [
            sympy.Eq(px + time * vx, pos.x + time * vec.x),
            sympy.Eq(py + time * vy, pos.y + time * vec.y),
            sympy.Eq(pz + time * vz, pos.z + time * vec.z),
        ]

    pprint(eqs)
    point = sympy.solve(eqs, syms)[0]
    pprint(point)

    return sum(point[:3])


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(((19, 13, 30), (-2, 1, -2)), parse(example)[0])

    def test_part1_example_answer(self):
        self.assertEqual(2, part1(parse(example)))

    # @unittest.skip
    def test_part1_answer(self):
        self.assertEqual(11098, part1(parse(data), (200000000000000, 400000000000000)))

    def test_part2_example_answer(self):
        self.assertEqual(47, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
