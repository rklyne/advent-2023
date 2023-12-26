import typing
import unittest
import itertools
import heapq

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


class Graph():
    _ignored: list[Edge]
    _emap: dict[Node, list[Node]]

    def __init__(self, edges: Input):
        self._emap = {}
        for a, b in edges:
            self._emap.setdefault(a, []).append(b)
            self._emap.setdefault(b, []).append(a)
        self._ignored = []

    def set_ignore(self, edges: list[Edge]):
        self._ignored = edges[:]

    def _next(self, src):
        return [
            n for n in self._emap[src]
            if (src, n) not in self._ignored
            if (n, src) not in self._ignored
        ]

    def shortest_path(self, src: Node, dest: Node) -> bool:
        SearchNode = tuple[int, Node, list[Node]]
        todo: list[SearchNode] = [(0, src, [])]
        heapq.heapify(todo)
        seen = set()
        while todo:
            cost, n, path = heapq.heappop(todo)
            if n in seen:
                continue
            seen.add(n)
            if n == dest:
                return path
            for m in self._next(n):
                heapq.heappush(todo, (cost + 1, m, path + [n]))
        return []


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


def find_cut_edges(input: Input):
    count = 0
    total = len(input)
    g = Graph(input)
    for a in input:
        count += 1
        g.set_ignore([a])
        path_one_cut = g.shortest_path(a[0], a[1])
        for edge in zip([a[0]] + path_one_cut, path_one_cut + [a[1]]):
            g.set_ignore([a, edge])
            path_two_cut = g.shortest_path(a[0], a[1])
            for edge2 in zip([a[0]] + path_two_cut, path_two_cut + [a[1]]):
                g.set_ignore([a, edge, edge2])
                path_three_cut = g.shortest_path(a[0], a[1])
                if not path_three_cut:
                    return [a, edge, edge2]
        print(f"done {count}/{total}")


def part1(input: Input):
    edges = find_cut_edges(input)
    a = edges[0]
    remaining = [
        e for e in input
        if e not in edges
        if tuple(reversed(e)) not in edges
    ]
    print(f"removed {edges}, leaving {remaining}")
    s1 = size(remaining, a[0])
    print(f"size {a[0]} is {s1}")
    return s1 * size(remaining, a[1])


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(("jqt", "rhn"), parse(example)[0])

    def test_part1_example_answer(self):
        self.assertEqual(54, part1(parse(example)))

    # @unittest.skip
    def test_part1_answer(self):
        self.assertEqual(-1, part1(parse(data)))


if __name__ == "__main__":
    unittest.main()
