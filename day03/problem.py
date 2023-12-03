import typing
import unittest
import re

from data import data, example


Input = list[str]
Span = typing.Tuple[int, typing.Tuple[int, int]]


def parse(input: str) -> Input:
    lines = ["." + l + "." for l in input.split("\n")]
    blank = "." * len(lines[0])
    return [blank] + lines + [blank]


digit = re.compile("[0-9]+")


def get_adjacent_ranges(n: Span) -> list[Span]:
    line = n[0]
    start = n[1][0]
    end = n[1][1]
    return [
        (line - 1, (start - 1, end + 1)),
        (line + 1, (start - 1, end + 1)),
        (line, (start - 1, start)),
        (line, (end, end + 1)),
    ]


def find_parts(input: Input, searcher: re.Pattern = digit) -> list[Span]:
    parts: list[Span] = []
    for y, line in enumerate(input):
        upto = 0
        while True:
            match = searcher.search(line, pos=upto)
            if not match:
                break
            start = match.span()[0]
            end = match.span()[1]
            parts.append((y, (start, end)))
            upto = end
    return parts


def read_input_span(input: Input, n: Span) -> str:
    line = n[0]
    start = n[1][0]
    end = n[1][1]
    return input[line][start:end]


def filter_parts(input: Input, f: typing.Callable[[str], bool]):
    parts = find_parts(input)
    parts_ids: list[str] = []
    for n in parts:
        string = read_input_span(input, n)
        ranges = get_adjacent_ranges(n)
        string_adjacent = "".join([input[r[0]][r[1][0] : r[1][1]] for r in ranges])
        if f(string_adjacent):
            parts_ids.append(string)
    return parts_ids


def span_in_spans(s0: Span, ss: list[Span]) -> bool:
    for s1 in ss:
        if s0[0] == s1[0]:
            r0 = s0[1]
            r1 = s1[1]
            if r0[0] >= r1[0] and r0[1] <= r1[1]:
                return True
    return False


def part1(input: Input):
    parts = filter_parts(input, lambda adj: adj.count(".") != len(adj))
    return sum(int(s) for s in parts)


def part2(input: Input):
    parts = find_parts(input)
    gears = find_parts(input, re.compile('\*'))
    total_ratio = 0
    for gear in gears:
        parts_adjacent = []
        for part in parts:
            if span_in_spans(gear, get_adjacent_ranges(part)):
                parts_adjacent.append(read_input_span(input, part))
        if len(parts_adjacent) == 2:
            total_ratio += int(parts_adjacent[0]) * int(parts_adjacent[1])
    return total_ratio


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(".467..114...", parse(example)[1])

    def test_part1_example_answer(self):
        self.assertEqual(4361, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(514969, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(467835, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(78915902, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
