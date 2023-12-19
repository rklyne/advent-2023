from typing import Literal, Tuple, Callable, Dict
from functools import reduce
from itertools import permutations
import operator

import typing
import unittest

from data import data, example


Name = str
Op = Literal["<", ">"]
Cond = Tuple[str, Op, int, Name]
Flow = Tuple[Name, list[Cond], Name]
Input = Tuple[int, int, int, int]  # x m a s
PuzzleInput = Tuple[list[Flow], list[Input]]


class Computer:
    letter_idx: Dict[Name, int] = {
        "x": 0,
        "m": 1,
        "a": 2,
        "s": 3,
    }

    def __init__(self, flows: list[Flow]):
        self.flows = flows
        self._flows = {
            f: self._mk_f(cs, d)
            for (f, cs, d) in flows
        }
        self._reverse = {
            d: self._mk_reverse(cs, f)
            for (f, cs, d) in flows
        }

    @classmethod
    def _mk_f(cls, cs: list[Cond], default: Name) -> Callable[[Input], Name]:
        matches = []
        for c in cs:
            if c[1] == ">":
                op = lambda n, i=cls.letter_idx[c[0]], x=c[2]: n[i]>x
            elif c[1] == "<":
                op = lambda n, i=cls.letter_idx[c[0]], x=c[2]: n[i]<x
            else:
                raise RuntimeError(c)
            matches.append((op, c[3]))

        def f(i: Input) -> Name:
            for _f, r in matches:
                if _f(i):
                    return r
            return default
        return f

    @classmethod
    def _mk_reverse(cls, cs: list[Cond], default: Name) -> Callable[[Input], Name]:
        matches = []
        for c in cs:
            if c[1] == ">":
                op = lambda n, i=cls.letter_idx[c[0]], x=c[2]: n[i]>x
            elif c[1] == "<":
                op = lambda n, i=cls.letter_idx[c[0]], x=c[2]: n[i]<x
            else:
                raise RuntimeError(c)
            matches.append((op, c[3]))

        def f(i: Input) -> Name:
            for _f, r in matches:
                if _f(i):
                    return r
            return default
        return f

    def process(self, instr: Input) -> int:
        pos = "in"
        while True:
            if pos == "A":
                return sum(instr)
            if pos == "R":
                return 0
            pos = self._flows[pos](instr)
        raise RuntimeError("bad looping")

    def paths_to(self, target, start="in"):
        MAX = 4000 + 1
        opts = [
            set(range(1, MAX))
            for c in 'xmas'
        ]
        todo = [start]
        while todo:
            name, flow, default = self._reversed_flows[todo.pop()]
            for char, op, const, to in flow:
                cidx = self.letter_idx[char]
                if op == "<":
                    op_set = set(range(1, const))
                else:
                    op_set = set(range(const+1, MAX))
                if to == 'R':
                    opts[cidx].difference_update(op_set)
                elif to == 'A':
                    # TODO: Somehtign somethign add to total here if ??? some condition?
                    opts[cidx].difference_update(op_set)
                else:
                    todo.add(to)
        return reduce(operator.mul, list(map(len, opts)), 1)


def parse(input: str) -> PuzzleInput:
    flows, inputs = input.split("\n\n")
    fs: list[Flow] = []
    for f in flows.replace("}", "").split("\n"):
        name, rest = f.split("{")
        rules: list[str] = rest.split(",")
        default = rules[-1]
        rules_bits: list[list[str]] = [r.split(":") for r in rules[:-1]]
        conds = [(c[0], c[1], int(c[2:]), to) for c, to in rules_bits]
        fs.append((name, conds, default))
    ins = []
    for in_line in inputs.split("\n"):
        parts = [p.split("=")[1] for p in in_line.replace("}", "").split(",")]
        ins.append(
            (
                int(parts[0]),
                int(parts[1]),
                int(parts[2]),
                int(parts[3]),
            )
        )
    return fs, ins


def part1(input: PuzzleInput):
    flows, inputs = input
    computer = Computer(flows)
    return sum(computer.process(i) for i in inputs)
    return 0


def part2(input: PuzzleInput):
    flows, inputs = input
    computer = Computer(flows)
    lines_by_char = {
        'x': [],
        'm': [],
        'a': [],
        's': [],
    }

    for flow_name, conds, default in flows:
        for char, op, num, to in conds:
            if op == ">":
                num += 1
            lines_by_char[char].append(num)
    pairs_by_char = {
        k: list(zip(v, v[1:]))
        for k, v in lines_by_char.items()
    }
    raise RuntimeError([len(v) for v in lines_by_char.values()])



class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(
            ("px", [("a", "<", 2006, "qkq"), ("m", ">", 2090, "A")], "rfg"),
            parse(example)[0][0],
        )
        self.assertEqual((787, 2655, 1222, 2876), parse(example)[1][0])

    def test_part1_example_answer(self):
        self.assertEqual(19114, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(446517, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(167409079868000, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
