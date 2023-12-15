from functools import lru_cache
from typing import Dict, Tuple
import typing
import unittest

from data import data, example


Input = list[str]


def parse(input: str) -> Input:
    return input.replace("\n", "").split(",")


def hash(s):
    total = 0
    for c in s:
        total = ((total + ord(c)) * 17) % 256
    return total


def part1(input: Input):
    return sum(map(hash, input))


Box = Tuple[list[str], list[int]]


def make_box() -> Box:
    return [], []


def remove_lens(box: Box, label: str) -> Box:
    try:
        idx = box[0].index(label)
    except ValueError:
        return box
    # MUTATION
    box[0].pop(idx)
    box[1].pop(idx)
    return box


def add_lens(box: Box, label: str, new_lens: int) -> Box:
    try:
        idx = box[0].index(label)
    except ValueError:
        box[0].append(label)
        box[1].append(new_lens)
    else:
        box[1][idx] = new_lens
    return box


def part2(input: Input):
    boxes: list[Box] = [make_box() for i in range(256)]
    for instr in input:
        if "-" in instr:
            label, _ = instr.split("-")
            box = hash(label)
            boxes[box] = remove_lens(boxes[box], label)
        elif "=" in instr:
            label, new_lens = instr.split("=")
            box = hash(label)
            boxes[box] = add_lens(boxes[box], label, int(new_lens))
        else:
            raise RuntimeError(instr)

    total = 0
    for n, box in enumerate(boxes, 1):
        for ln, lens in enumerate(box[1], 1):
            total += n * ln * lens

    return total


class Tests(unittest.TestCase):
    @unittest.skip
    def test_parse(self):
        self.assertEqual("-", parse(example))

    def test_part1_example_answer(self):
        self.assertEqual(1320, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(519603, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(145, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(244342, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
