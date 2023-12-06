import typing
import unittest
import math

from data import data, example

Time = int
Distance = int
Race = typing.Tuple[Time, Distance]
Input = list[Race]


def parse(input: str) -> Input:
    lines = [filter(bool, l.split(":")[1].split(" ")) for l in input.split("\n")]
    times = map(int, lines[0])
    distances = map(int, lines[1])
    return list(zip(times, distances))


def get_roots(time, record) -> [int, int]:
    """
    speed = press
    # solve for
    0 = (time - press) * speed - record
    0 = time * press - press^2 - record
    0 = - press^2 + time * press - record

    press = (-time +- sqrt(time^2 - (4 * distance))) / -2
    """
    ns = sorted([
        ((-time) - math.sqrt((time**2) - (4 * record))) / -2,
        ((-time) + math.sqrt((time**2) - (4 * record))) / -2,
    ])
    # print(f"({time}, {record}) -> {ns}")
    lower = math.ceil(ns[0])
    if lower == ns[0]:
        lower += 1
    upper = math.floor(ns[1])
    if upper == ns[1]:
        upper -= 1
    return lower, upper


def get_win_ways(time, record) -> int:
    l, u = get_roots(time, record)
    return (u - l) + 1


def part1(input: Input):
    total = 1
    for time, record in input:
        total *= get_win_ways(time, record)
    return total


def part2(input: Input):
    times, records = zip(*input)
    time = int("".join(map(str, times)))
    record = int("".join(map(str, records)))
    return get_win_ways(time, record)


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual((7, 9), parse(example)[0])

    def test_roots(self):
        self.assertEqual((2, 5), get_roots(7, 9))

    def test_win_counts(self):
        self.assertEqual(4, get_win_ways(7, 9))
        self.assertEqual(8, get_win_ways(15, 40))
        self.assertEqual(9, get_win_ways(30, 200))

    def test_part1_example_answer(self):
        self.assertEqual(288, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(608902, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(71503, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(46173809, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
