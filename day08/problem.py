from typing import Dict, Tuple, Callable
from itertools import cycle
from functools import reduce
import math

import typing
import unittest

from data import data, example, example2, example3


Direction = typing.Literal["L", "R"]
Node = str
Branch = typing.Tuple[Node, typing.Tuple[Node, Node]]
Path = str
Input = typing.Tuple[Path, list[Branch]]


def parse(input: str) -> Input:
    path, nodes = input.split("\n\n")
    branches = [
        eval("('" + n.replace(" = ", "',").replace("(", "('").replace(")", "')").replace(", ", "','") + ")")
        for n in nodes.split("\n")
    ]

    return path, branches


class NodeMap():
    nodes: Dict[Node, Tuple[Node, Node]]
    branches: list[Branch]

    def __init__(self, branches: list[Branch]):
        self.branches = branches
        self.nodes = {
            src: dests
            for (src, dests) in branches
        }

    @staticmethod
    def _choose(pair: Tuple[Node, Node], d: Direction):
        if d == "L":
            return pair[0]
        else:
            return pair[1]

    def navigate(self, node: Node, step: Direction) -> Node:
        return self._choose(self.nodes[node], step)


START = "AAA"
END = "ZZZ"


def part1(input: Input) -> int:
    return solve(input, START, lambda x: x == END)


def solve(input: Input, start: Node, is_end: Callable[[Node], bool]) -> int:
    path = input[0]
    m = NodeMap(input[1])
    current = start
    steps = cycle(path)
    count = 0
    while not is_end(current):
        count += 1
        current = m.navigate(current, next(steps))
    return count


def part2(input: Input):
    starts = [n for (n, _) in input[1] if n.endswith("A")]
    is_end = lambda n: n.endswith("Z")
    counts = [solve(input, start, is_end) for start in starts]
    # raise RuntimeError(counts)
    return reduce(math.lcm, counts)


class Tests(unittest.TestCase):
    def test_parse(self):
        path, branches = parse(example)
        self.assertEqual("RL", path)
        self.assertEqual(("AAA", ("BBB", "CCC")), branches[0])

    def test_part1_example_answer(self):
        self.assertEqual(2, part1(parse(example)))

    def test_part1_example2_answer(self):
        self.assertEqual(6, part1(parse(example2)))

    def test_part1_answer(self):
        self.assertEqual(20513, part1(parse(data)))

    def test_part2_example3_answer(self):
        self.assertEqual(6, part2(parse(example3)))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
