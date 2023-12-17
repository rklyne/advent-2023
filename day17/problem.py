from typing import Tuple, Literal, Union, Dict
import typing
import unittest
import heapq

from data import data, example


Input = list[list[int]]


def parse(input: str) -> Input:
    return [list(map(int, line)) for line in input.split("\n")]


U = (-1, 0)
D = (1, 0)
L = (0, -1)
R = (0, 1)
Cost = int
Coord = Tuple[int, int]
Direction = Literal[U, D, L, R]
Node = Tuple[Coord, Direction]
Path = list[Node]
SearchNode = Tuple[Cost, Cost, Node, Path]  # cost, place, history

turn_left = {
    L: D,
    D: R,
    R: U,
    U: L,
}
turn_right = {v: k for k, v in turn_left.items()}


def move(node: Node, d: Direction) -> Node:
    pos = node[0]
    return (
        (
            pos[0] + d[0],
            pos[1] + d[1],
        ),
        d,
    )


def part1(board: Input) -> int:
    to_search: list[SearchNode] = [
        (0, 0, ((0, 0), R), []),
        (0, 0, ((0, 0), D), []),
    ]
    max_row = len(board)
    max_col = len(board[0])
    destination = max_row - 1, max_col - 1
    heapq.heapify(to_search)
    cheapest_node_route: Dict[Node, Cost] = {}
    best_yet: Cost = 99999999
    best_solution: Path = []
    tries = 0
    solutions = 0
    shortcuts = 0

    def make_move(current: SearchNode, d: Direction):
        _, cost, node, path = current
        new_node = move(node, d)  # forward
        new_pos = new_node[0]
        if new_pos[0] < 0 or new_pos[0] >= max_row:
            return
        if new_pos[1] < 0 or new_pos[1] >= max_col:
            return
        last_three_moves = [node[1] for node in path[-3:]]
        if len(set(last_three_moves)) == 1 and last_three_moves[0] == d:
            return
        new_tile = board[new_pos[0]][new_pos[1]]
        new_cost = new_tile + cost
        new_path = path[:] + [new_node]
        priority = new_cost
        new_search_node: SearchNode = (priority, new_cost, new_node, new_path)
        heapq.heappush(to_search, new_search_node)

    while to_search:
        tries += 1
        search_node = heapq.heappop(to_search)
        _, cost, node, path = search_node
        if tries >= 2800000:
            print("OVERFLOW")
            break
        if node in cheapest_node_route and cheapest_node_route[node] < cost:
            shortcuts += 1
            continue
        cheapest_node_route[node] = cost
        pos, facing = node
        if pos == destination:
            solutions += 1
            if cost < best_yet:
                best_yet = cost
                best_solution = path
            continue
        make_move(search_node, facing)
        make_move(search_node, turn_left[facing])
        make_move(search_node, turn_right[facing])

    # print(f"{best_yet} ({tries}): {best_solution}")
    # print(f"debug: {len(cheapest_node_route)}")
    print(f"PATH {best_yet} ({solutions}/{shortcuts}): {[(board[n[0]][n[1]], d) for n, d in best_solution]}")
    return best_yet


def part2(input: Input):
    return 0


TINY1 = """
222
222
622
""".strip()


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual([2, 4, 1, 3, 4, 3, 2, 3, 1, 1, 3, 2, 3], parse(example)[0])

    def test_move(self):
        self.assertEqual(((0, 1), R), move(((0, 0), D), R))

    def test_part1_a_tiny_1(self):
        self.assertEqual(8, part1(parse(TINY1)))

    def test_part1_example_answer(self):
        self.assertEqual(102, part1(parse(example)))

    @unittest.skip
    def test_part1_real_answer(self):
        self.assertEqual(-1, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(-1, part2(parse(example)))

    @unittest.skip
    def test_part2_real_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
