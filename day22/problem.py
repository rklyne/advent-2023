from typing import NewType, NamedTuple
from pprint import pprint
import typing
import unittest
from functools import lru_cache

from data import data, example


X = NewType("X", int)
Y = NewType("Y", int)
Z = NewType("Z", int)


class Coord(NamedTuple):
    x: X
    y: Y
    z: Z

    def __repr__(self):
        return f"c(x{self.x}, y{self.y}, z{self.z})"


Block = tuple[Coord, Coord]
BlockId = int
Input = list[Block]


FLOOR = -1


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
    _supported_by: dict[BlockId, list[BlockId]]
    _supporting: dict[BlockId, list[BlockId]]

    def __init__(self, maxx, maxy, maxz):
        self.maxx = maxx
        self.maxy = maxy
        self.maxz = maxz
        self._blank()
        self._blocks = {}
        self._supported_by = {-1: []}
        self._supporting = {-1: []}

    def _blank(self):
        self._space = [
            [[FLOOR] + ([0] * (self.maxz + 1)) for y in range(self.maxy + 1)]
            for x in range(self.maxx + 1)
        ]

    def _set(self, c: Coord, block_id: BlockId):
        self._space[c.x][c.y][c.z] = block_id

    @lru_cache
    def _cube_fall_dist(self, cube: Coord, ignore: tuple[BlockId] = set()) -> int:
        ignores = set(ignore).union([0])
        col = self._space[cube.x][cube.y]
        zrange = list(range(cube.z - 1, -1, -1))
        for z in zrange:
            if col[z] not in ignores:
                d = (cube.z - z) - 1
                return d
        return cube.z

    def _block_fall_dist(self, block: Block, ignore: set[BlockId] = set()) -> int:
        dist = min(
            map(
                lambda c: self._cube_fall_dist(c, ignore=tuple(ignore)),
                self._cubes(block),
            )
        )
        return dist

    def could_fall_without(self, block_ids: list[BlockId], recurse=False):
        # TODO: filter to blocks this is supporting that now have no support
        fallers = set([b for b in self._supporting[block_ids[-1]] if not set(self._supported_by[b]).difference(block_ids)])
        if recurse:
            for f in list(fallers):
                fallers.update(self.could_fall_without(block_ids + list(fallers) + [f], True))
        return fallers

    def _blocks_in_space(self, block: Block, at_z: int) -> set[BlockId]:
        blocks = set()

        def _mk_range(a, b):
            i, j = sorted([a, b])
            return i, j+1

        for x in range(*_mk_range(block[0].x, block[1].x)):
            for y in range(*_mk_range(block[0].y, block[1].y)):
                blocks.add(self._space[x][y][at_z])
        return blocks.difference([0])

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
        fall_dist = self._block_fall_dist(block)
        if fall_dist:
            c1, c2 = block
            if fall_dist > c1.z:
                raise RuntimeError(c1, c2, fall_dist, self._blocks)
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
        # print(f">>> added {block_id} @{block}")
        self._blocks[block_id] = block
        self._supporting[block_id] = []
        self._supported_by[block_id] = list(self._blocks_in_space(
            block, min(block[0].z, block[1].z) - 1
        ))
        for id in self._supported_by[block_id]:
            self._supporting[id].append(block_id)

    def _zrange(self):
        return range(0, self.maxz)

    def pprint(self):
        for layer in zip(*map(lambda ls: zip(*ls), self._space)):
            if not any(map(any, layer)):
                continue
            print("\n".join([" ".join([str(i).zfill(3) for i in l]) for l in layer]))
            print("---")


def _blocks_with_ids(blocks: list[Block]) -> list[tuple[BlockId, Block]]:
    return list(enumerate(blocks, 1))


def part1(input: Input):
    blocks = list(sorted(input, key=lambda b: min(b[0].z, b[1].z)))

    xs, ys, zs = zip(*([b[0] for b in blocks] + [b[1] for b in blocks]))
    # print(f"({min(xs)}, {max(xs)}) ({min(ys)}, {max(ys)}) ({min(zs)}, {max(zs)}) ")

    space = BlockSpace(max(xs), max(ys), max(zs))
    for block_id, block in _blocks_with_ids(blocks):
        space.add_block(block, block_id)

    # print(f"{space._supported_by}")
    # print(f"{space._supporting}")
    count = 0
    for remove_block, block in _blocks_with_ids(blocks):
        if not space.could_fall_without([remove_block]):
            count += 1

    return count


def part2(input: Input):
    blocks = list(sorted(input, key=lambda b: min(b[0].z, b[1].z)))
    xs, ys, zs = zip(*([b[0] for b in blocks] + [b[1] for b in blocks]))

    space = BlockSpace(max(xs), max(ys), max(zs))
    for block_id, block in _blocks_with_ids(blocks):
        space.add_block(block, block_id)

    count = 0
    for remove_block, block in _blocks_with_ids(blocks):
        fallers = len(space.could_fall_without([remove_block], recurse=True))
        count += fallers

    return count


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(((1, 0, 1), (1, 2, 1)), parse(example)[0])

    # @unittest.skip
    def test_part1_example_answer(self):
        self.assertEqual(5, part1(parse(example)))

    # @unittest.skip
    def test_part1_answer(self):
        # 544 too high
        self.assertEqual(451, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(7, part2(parse(example)))

    # @unittest.skip
    def test_part2_answer(self):
        # takes a minute but it's right
        self.assertEqual(66530, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
