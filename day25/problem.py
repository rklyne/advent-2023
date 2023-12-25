import typing
import unittest
import itertools

from data import data, example


Node = str
Edge = tuple[Node, Node]
Input = list[Edge]


def parse(input: str) -> Input:
    def _parse():
        for line in input.split("\n"):
            src, dests = line.split(": ")
            for dest in dests.split(" "):
                yield (src, dest)
    return list(_parse())


def shortest_path(edges: Input, src: Node, dest: Node) -> bool:
    e_map = {}
    for a, b in edges:
        e_map.setdefault(a, []).append(b)
        e_map.setdefault(b, []).append(a)
    todo = [src]
    seen = set()
    while todo:
        n = todo.pop()
        if n in seen:
            continue
        seen.add(n)
        if n == dest:
            return True
        for m in e_map[n]:
            todo.append(m)
    return False


def size(edges: Input, src: Node) -> int:
    e_map = {}
    for a, b in edges:
        e_map.setdefault(a, []).append(b)
        e_map.setdefault(b, []).append(a)
    todo = [src]
    seen = set()
    while todo:
        n = todo.pop()
        if n in seen:
            continue
        seen.add(n)
        for m in e_map[n]:
            todo.append(m)
    return len(seen)


def part1(input: Input):
    for a, b, c in itertools.combinations(input, 3):
        remaining = [
            n for n in input
            if n not in [a, b, c]
        ]
        if not shortest_path(remaining, a[0], a[1]):
            return size(remaining, a[0]) * size(remaining, a[1])
    return 0


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(("jqt", "rhn"), parse(example)[0])

    def test_part1_example_answer(self):
        self.assertEqual(54, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(-1, part1(parse(data)))


if __name__ == "__main__":
    unittest.main()
