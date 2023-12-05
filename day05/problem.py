from typing import Tuple, Iterable
import unittest

from data import data, example


Range = Tuple[int, int]
MapLine = Tuple[int, int, int]
Mapping = list[MapLine]
Seed = int
Input = Tuple[list[Seed], list[Mapping]]


def threeple(xs_iter: Iterable[int]) -> MapLine:
    xs = list(xs_iter)
    return xs[0], xs[1], xs[2]


def parse(input: str) -> Input:
    chunks = input.split("\n\n")
    seed_txt = chunks[0][7:]

    def parse_mapping(txt: str) -> Mapping:
        return [threeple(map(int, line.split(" "))) for line in txt.split("\n")[1:]]

    maps = map(parse_mapping, chunks[1:])
    return (list(map(int, seed_txt.split(" "))), list(maps))


def map_value(value: int, ms: Mapping) -> int:
    for dst, src, l in ms:
        if value >= src and value < src + l:
            return value - src + dst
    return value


def map_value_reverse(value: int, ms: Mapping) -> int:
    return map_value(value, [(src, dst, l) for dst, src, l in ms])


def map_all(item: int, mappings: list[Mapping]) -> int:
    for m in mappings:
        item = map_value(item, m)
    return item


def map_all_reverse(item: int, mappings: list[Mapping]) -> int:
    for m in reversed(mappings):
        item = map_value_reverse(item, m)
    return item


def part1(input: Input):
    mapping: list[Mapping] = input[1]

    def map_item(item: int) -> int:
        return map_all(item, mapping)

    locations = map(map_item, input[0])
    return min(locations)


def in_ranges(n: int, rs: list[Range]):
    for start, l in rs:
        if n >= start and n < start + l:
            return True
    return False


def part2(input: Input, init_pad: int = 0):
    mappings: list[Mapping] = input[1]
    to_reverse: list[Mapping] = []

    all_numbers: list[int] = []
    for mapping in mappings:
        for dst, start, l in mapping:
            all_numbers.append(map_all_reverse(start, to_reverse))
        to_reverse.append(mapping)

    seed_pairs: list[Range] = []
    seed_ranges = input[0][:]
    seeds = set(all_numbers)
    while seed_ranges:
        start, count = seed_ranges[0:2]
        seed_pairs.append((start, count))
        seed_ranges = seed_ranges[2:]
        for n in all_numbers:
            if n >= start and n <= start + count:
                seeds.add(n)

    def map_all_input(item: int):
        return map_all(item, mappings)

    locations = map(
        map_all_input,
        filter(
            lambda s: in_ranges(s, seed_pairs), [s for s in seeds]
        )
    )
    return min(locations)


class Tests(unittest.TestCase):
    def test_map_value_unchanged(self):
        self.assertEqual(10, map_value(10, []))

    def test_map_value_in_range(self):
        self.assertEqual(20, map_value(10, [(20, 10, 2)]))

    def test_map_value_past_range(self):
        self.assertEqual(12, map_value(12, [(20, 10, 2)]))

    def test_part1_parse(self):
        parsed = parse(example)
        self.assertEqual([79, 14, 55, 13], parsed[0])
        self.assertEqual([(50, 98, 2), (52, 50, 48)], parsed[1][0])

    def test_part1_example_answer(self):
        self.assertEqual(35, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(282277027, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(46, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(11554135, part2(parse(data), 0))

    def test_map_reverse(self):
        ms = parse(data)[1]
        n = 282277027
        self.assertEqual(n, map_all(map_all_reverse(n, ms), ms))


if __name__ == "__main__":
    unittest.main()
