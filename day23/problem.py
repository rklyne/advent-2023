import typing
from typing import Iterable, Dict, Callable
import unittest
import itertools
from pprint import pprint

from data import data, example


Tiles = list[str]
Input = Tiles
Coord = tuple[int, int]

Node = Coord
Cost = int
Edge = tuple[Node, Node, Cost]
Graph = list[Edge]

START = (0, 1)
ROCK = "#"


def parse(input: str) -> Input:
    return input.split("\n")


def adjacent(n: Node) -> set[Node]:
    return set(
        [
            (n[0] + 1, n[1]),
            (n[0] - 1, n[1]),
            (n[0], n[1] + 1),
            (n[0], n[1] - 1),
        ]
    )


def clamp_to_grid(grid: Tiles, nodes: Iterable[Node]) -> list[Node]:
    maxrow = len(grid)
    maxcol = len(grid[0])
    return [
        n for n in nodes if n[0] >= 0 and n[0] < maxrow if n[1] >= 0 and n[1] < maxcol
    ]


def read_tile(tiles: Tiles, n: Node) -> str:
    r, c = n
    return tiles[r][c]


def make_graph(tiles: Tiles) -> Graph:
    Search = tuple[Node, int, Node, bool]
    walks: list[Search] = [(START, 0, START, True)]
    seen: set[Node] = set()
    rocks: set[Node] = set(
        [
            (r, c)
            for r, row in enumerate(tiles)
            for c, tile in enumerate(row)
            if tile == ROCK
        ]
    )
    edges: Graph = []

    next_validator: Dict[str, Callable[[Node, Node], bool]] = {
        # TODO: maybe "<" instead of "<=" ?
        ">": lambda a, b: a[1] <= b[1],
        "<": lambda a, b: a[1] >= b[1],
        "v": lambda a, b: a[0] <= b[0],
        "^": lambda a, b: a[0] >= b[0],
        ".": lambda a, b: True,
    }
    while walks:
        start, cost, prev, one_way = walks.pop()
        seen.add(prev)
        tile = read_tile(tiles, prev)
        if tile in "<>v^":
            one_way = True
        nexts = clamp_to_grid(
            tiles, adjacent(prev).difference([prev]).difference(seen).difference(rocks)
        )
        if len(nexts) == 1:
            walks.append((start, cost + 1, nexts[0], one_way))
        else:
            edges.append((start, prev, cost))
            if not one_way:
                edges.append((prev, start, cost))
            for n in nexts:
                next_tile = read_tile(tiles, n)
                if next_validator[next_tile](prev, n):
                    walks.append((prev, 0, n, False))
    return edges


def part1(input: Input):
    graph = make_graph(input)
    END = (len(input) - 1, len(input[0]) - 2)
    best = 0
    route_count = 0
    RoutePlan = tuple[Node, int, list[Node]]
    routes: list[RoutePlan] = [(START, 0, [])]
    best_path = []
    all_paths = []
    logs: list[str] = []
    log = logs.append
    most_routes = 1
    while routes:
        most_routes = max(most_routes, len(routes))
        current, cost, seen = routes.pop()
        if current == END:
            log(f"Path reached end: {seen}")
            all_paths.append(seen)
            route_count += 1
            if cost > best:
                best = max(best, cost)
                log(f"Path is best yet: {best}")
                best_path = seen
            continue
        edges: list[Edge] = [e for e in graph if e[0] == current]
        new_seen = seen + [current]
        added = 0
        log(f"edges from {current}: {edges}")
        for here, there, dist in edges:
            if there not in seen:
                added += 1
                routes.append((there, cost + dist, new_seen))
    print(f"best {best} of {route_count} / {most_routes}: {best_path}")
    # pprint({"graph": graph})
    # pprint(all_paths)
    pprint(logs)
    return best


def part2(input: Input):
    return 0


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual("#.......#########...###", parse(example)[1])

    def test_graph(self):
        graph = make_graph(parse(example))
        self.assertEqual(((0, 1), (5, 3), 15), graph[0])

    def test_part1_example_answer(self):
        self.assertEqual(94, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(-1, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(-1, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
