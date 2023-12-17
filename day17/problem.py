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
dir_names: Dict[Direction, str] = {
    L: "L",
    D: "d",
    R: "R",
    U: "U",
}


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
    return find_cost(board, 1, 3)


def find_cost(board: Input, min_straight_line: int, max_straight_line: int, LIMIT: int = 800000, PRINT: bool = False) -> int:
    to_search: list[SearchNode] = [
        (0, 0, ((0, 0), R), []),
        (0, 0, ((0, 0), D), []),
    ]
    max_row = len(board)
    max_col = len(board[0])
    destination = max_row - 1, max_col - 1
    heapq.heapify(to_search)
    cheapest_node_route: Dict[Node, Cost] = {}
    MAX_COST = 99999999
    best_yet: Cost = MAX_COST
    best_solution: Path = []
    tries = 0
    solutions = 0
    shortcuts = 0

    def heuristic(pos: Coord):
        return (destination[0] - pos[0]) + (destination[1] - pos[1])

    def make_move(current: SearchNode, d: Direction):
        _, cost, node, path = current
        last_three_moves = [node[1] for node in path[-max_straight_line:]]
        if last_three_moves == [d] * max_straight_line:
            # If we did 3 moves in this direction then we can't do another
            return
        new_node = move(node, d)  # forward
        new_pos = new_node[0]
        if new_pos[0] < 0 or new_pos[0] >= max_row:
            return
        if new_pos[1] < 0 or new_pos[1] >= max_col:
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
        if tries >= LIMIT:
            print("OVERFLOW")
            break
        path_len = 0
        if path:
            d = path[-1][1]
            for n in reversed(path[:-1]):
                if n[1] != d:
                    break
                path_len += 1
            if path_len > max_straight_line:
                continue
        # cache_key = (path_len, node)
        cache_key = node
        if path_len < 1:
            cheapest = cheapest_node_route.get(cache_key, MAX_COST)
            if cheapest <= cost:
                shortcuts += 1
                continue
            cheapest_node_route[node] = cost + path_len
        pos, facing = node
        if pos == destination and (path_len + 1 >= min_straight_line):
            solutions += 1
            if cost < best_yet:
                best_yet = cost
                best_solution = path
            continue
        make_move(search_node, facing)
        if path_len + 1 >= min_straight_line:
            make_move(search_node, turn_left[facing])
            make_move(search_node, turn_right[facing])

    # print(f"{best_yet} ({tries}): {best_solution}")
    # print(f"debug: {len(cheapest_node_route)}")
    # print(f"PATH {best_yet} ({solutions}/{shortcuts}): {[(board[n[0]][n[1]], d) for n, d in best_solution]}")
    # print(f"SUM {best_yet} ({solutions}/{shortcuts}): {sum([board[n[0]][n[1]] for n, _ in best_solution])}")
    if PRINT:
        print(
            f"PATH NAME {best_yet} ({solutions}/{shortcuts}/{tries}): {''.join(dir_names[d] for n, d in best_solution)}"
        )

    return best_yet


def part2(board: Input):
    return find_cost(board, 4, 10, LIMIT=2_000_000, PRINT=True)


TINY1 = """
222
222
622
""".strip()

SILLY1 = """
111111111111
999999999991
999999999991
999999999991
999999999991
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

    def test_part1_real_answer(self):
        # too low 1226
        # wrong - 1258
        # too high 1262
        # too high 1287
        self.assertEqual(1246, part1(parse(data)))

    def test_part1_a_silly_1(self):
        self.assertEqual(71, part2(parse(SILLY1)))

    def test_part2_example_answer(self):
        self.assertEqual(94, part2(parse(example)))

    def test_part2_real_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
