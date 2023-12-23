from typing import NewType, NamedTuple
from pprint import pprint
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

    def __init__(self, maxx, maxy, maxz):
        self.maxx = maxx
        self.maxy = maxy
        self.maxz = maxz
        self._blank()
        self._blocks = {}

    def _blank(self):
        self._space = [
            [[FLOOR] + ([0] * (self.maxz + 1)) for y in range(self.maxy + 1)]
            for x in range(self.maxx + 1)
        ]

    def _set(self, c: Coord, block_id: BlockId):
        self._space[c.x][c.y][c.z] = block_id

    def _cube_fall_dist(self, cube: Coord, ignore: set[BlockId] = set()) -> int:
        ignores = ignore.union([0])
        col = self._space[cube.x][cube.y]
        zrange = list(range(cube.z - 1, -1, -1))
        for z in zrange:
            if col[z] not in ignores:
                d = (cube.z - z) - 1
                return d
        return cube.z

    def _block_fall_dist(self, block: Block, ignore: set[BlockId] = set()) -> int:
        dist = min(
            map(lambda c: self._cube_fall_dist(c, ignore=ignore), self._cubes(block))
        )
        # print(f"{dist}, {block}")
        return dist

    def could_fall_without(self, block_id: BlockId):
        ignore = set([block_id])
        candidates = set()
        block = self._blocks[block_id]
        block_top = max(block[0].z, block[1].z)
        for x in range(0, self.maxx):
            for y in range(0, self.maxy):
                candidates.add(self._space[x][y][block_top + 1])
        candidates.difference_update([0])
        # candidates = set(self._blocks.keys())
        for other_id in candidates:
            other_block = self._blocks[other_id]
            if self._block_fall_dist(other_block, ignore.union(set([other_id]))) != 0:
                assert self._block_fall_dist(other_block) == 0, f"shouldn't fall without any change? ({other_id})"
                return True
        return False

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

    def _zrange(self):
        return range(0, self.maxz)

    def pprint(self):
        for layer in zip(*map(lambda ls: zip(*ls), self._space)):
            if not any(map(any, layer)):
                continue
            print("\n".join([' '.join([str(i).zfill(3) for i in l]) for l in layer]))
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

    space.pprint()

    count = 0
    removed = []
    for remove_block, block in _blocks_with_ids(blocks):
        if not space.could_fall_without(remove_block):
            count += 1
            removed.append(remove_block)
    print(f"blast: {removed}")

    return count


def part2(input: Input):
    return 0


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(((1, 0, 1), (1, 2, 1)), parse(example)[0])

    def test_part1_example_answer(self):
        self.assertEqual(5, part1(parse(example)))

    # @unittest.skip
    def test_part1_answer(self):
        # 544 too high
        self.assertEqual(-1, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(-1, part2(parse(example)))

    @unittest.skip
    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
