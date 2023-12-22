from typing import NewType, NamedTuple
import typing
import unittest

from data import data, example


X = NewType("X", int)
Y = NewType("Y", int)
Z = NewType("Z", int)


class Coord(NamedTuple):
    x: X
    y: Y
    z: Z


Block = tuple[Coord, Coord]
BlockId = int
Input = list[Block]


def parse(input: str) -> Input:
    def c(s):
        p = s.split(",")
        return Coord(X(int(p[0])), Y(int(p[1])), Z(int(p[2])))

    def _parse():
        for line in input.split("\n"):
            a, b = line.split("~")
            yield c(a), c(b)

    return list(_parse())


class BlockSpace:
    _space: list[list[list[BlockId]]]
    _blocks: dict[BlockId, Block]

    def __init__(self, maxx, maxy, maxz):
        self.maxx = maxx
        self.maxy = maxy
        self.maxz = maxz
        self._blank()
        self._blocks = {}

    def _blank(self):
        self._space = [
            [[0] * self.maxz for y in range(self.maxy + 1)]
            for x in range(self.maxx + 1)
        ]

    def _set(self, c: Coord, block_id: BlockId):
        self._space[c.x][c.y][c.z] = block_id

    def _cube_fall_dist(self, cube: Coord) -> int:
        col = self._space[cube.x][cube.y]
        for z in range(cube.z - 1, -1, -1):
            if col[z]:
                return cube.z - z + 1
        return cube.z
        raise NotImplementedError("todo - how far does this cube fall?")

    @staticmethod
    def _cubes(block: Block) -> list[Coord]:
        c1, c2 = block
        xs = list(sorted([c1.x, c2.x]))
        ys = list(sorted([c1.y, c2.y]))
        zs = list(sorted([c1.z, c2.z]))
        results: list[Coord] = []
        for x in range(xs[0], xs[1] + 1):
            nx = X(x)
            for y in range(ys[0], ys[1] + 1):
                ny = Y(y)
                for z in range(zs[0], zs[1] + 1):
                    nz = Z(z)
                    results.append(Coord(nx, ny, nz))
        return results

    def _fall(self, block: Block) -> Block:
        fall_dist = min(map(self._cube_fall_dist, self._cubes(block)))
        if fall_dist:
            c1, c2 = block
            return (
                Coord(c1.x, c1.y, Z(c1.z - fall_dist)),
                Coord(c2.x, c2.y, Z(c2.z - fall_dist)),
            )
        return block

    def add_block(self, block: Block, block_id: BlockId, fall=True):
        if fall:
            block = self._fall(block)
        for cube in self._cubes(block):
            self._set(cube, block_id)
        self._blocks[block_id] = block


def part1(input: Input):
    blocks = list(sorted(input, key=lambda b: min(b[0].z, b[1].z)))

    xs, ys, zs = zip(*([b[0] for b in blocks] + [b[1] for b in blocks]))
    print(f"({min(xs)}, {max(xs)}) ({min(ys)}, {max(ys)}) ({min(zs)}, {max(zs)}) ")

    space = BlockSpace(max(xs), max(ys), max(zs))
    for block_id, block in enumerate(blocks):
        space.add_block(block, block_id)

    count = 0
    for remove_block in blocks:
        if not space.could_fall_without(remove_block):
            count += 1

    return count


def part2(input: Input):
    return 0


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(((1, 0, 1), (1, 2, 1)), parse(example)[0])

    def test_part1_example_answer(self):
        self.assertEqual(-1, part1(parse(example)))

    @unittest.skip
    def test_part1_answer(self):
        self.assertEqual(-1, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(-1, part2(parse(example)))

    @unittest.skip
    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
