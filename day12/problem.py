from typing import Tuple, Dict, Iterable, Literal
from functools import lru_cache
import typing
import unittest
import re

from data import data, example


Input = list[Tuple[str, list[int]]]


def parse(input: str) -> Input:
    lines = [l.split(" ", 1) for l in input.split("\n")]
    return [(t, list(map(int, ns.split(",")))) for t, ns in lines]


def perm(line: str) -> Iterable[str]:
    qs = line.count("?")
    for i in range(2**qs):
        l: str = line
        while i:
            if i & 1:
                l = l.replace("?", "#", 1)
            else:
                l = l.replace("?", ".", 1)
            i >>= 1
        yield l.replace("?", ".")


def match_count_regex(line: str, nums: list[int]) -> int:
    ROCK = lambda n: f"[#]{{{n}}}"
    ANY_SPACE = re.escape("?") + "*"
    expr_str = "^" + "".join([ANY_SPACE + ROCK(n) for n in nums]) + ANY_SPACE + "$"
    expr = re.compile(expr_str)
    print(expr_str)
    total = 0
    for l in perm(line):
        if expr.match(l):
            print(f"GET {line} -> {l}")
            total += 1
        else:
            print(f"try {line} -> {l}")
    print(f" line: {line} nums: {nums} total: {total}")
    return total


maybe_rock = "#?"
maybe_gap = ".?"


@lru_cache(1000000000)
def all_gap(s: str) -> bool:
    return all(c in maybe_gap for c in s)


@lru_cache(1000000000)
def all_rock(s: str) -> bool:
    return all(c in maybe_rock for c in s)


@lru_cache(1000000)
def match_count(line: str, nums: Iterable[int]) -> int:
    if not nums:
        return 1 if all_gap(line) else 0
    if sum(nums) + len(nums) >= len(line):
        return 0
    if line[0] not in maybe_gap:
        return 0
    total = 0
    line = line[1:]
    if not line:
        return 0
    if line[0] in maybe_rock:
        if all_rock(line[: nums[0]]):
            total += match_count(line[nums[0]:], nums[1:])
    if line[0] in maybe_gap:
        next_step = 9999
        for c in maybe_rock:
            f = line.find(c)
            if f != -1 and f < next_step:
                next_step = f
        total += match_count(line, nums)
    return total


def part1(input: Input):
    total = 0
    for line, nums in input:
        total += match_count("." + line + ".", tuple(nums))
    return total


def part2(input: Input):
    total = 0
    for line, nums in input:
        total += match_count("." + (line + "?") * 4 + line + ".", tuple(nums * 5))
    return total


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(("???.###", [1, 1, 3]), parse(example)[0])

    def test_match_line(self):
        self.assertEqual(10, part1(parse("?###???????? 3,2,1")))
        self.assertEqual(1, part1(parse("???.### 1,1,3")))
        # self.assertEqual(10, part1(parse("?###???????? 3,2,1")))

    def test_part1_example_answer(self):
        self.assertEqual(21, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(7705, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(525152, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(50338344809230, part2(parse(data)))
        pass


if __name__ == "__main__":
    unittest.main()
