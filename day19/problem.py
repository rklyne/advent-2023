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
    MAX = 4000 + 1
    _reversed_flows: Dict[Name, list[Name]]
    _flows: Dict[Name, Flow]
    letter_idx: Dict[Name, int] = {
        "x": 0,
        "m": 1,
        "a": 2,
        "s": 3,
    }

    def __init__(self, flows: list[Flow]):
        self.flows = flows
        self._flows = {f[0]: f for f in flows}
        self._flow_functions = {f: self._mk_f(cs, d) for (f, cs, d) in flows}
        self._reversed_flows = {}
        for f, cs, d in flows:
            for c in cs:
                self._reversed_flows.setdefault(c[3], []).append(f)
            self._reversed_flows.setdefault(d, []).append(f)

    @classmethod
    def _mk_f(cls, cs: list[Cond], default: Name) -> Callable[[Input], Name]:
        matches = []
        for c in cs:
            if c[1] == ">":
                op = lambda n, i=cls.letter_idx[c[0]], x=c[2]: n[i] > x
            elif c[1] == "<":
                op = lambda n, i=cls.letter_idx[c[0]], x=c[2]: n[i] < x
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
            pos = self._flow_functions[pos](instr)
        raise RuntimeError("bad looping")

    def forward_paths(self, start="in") -> int:
        opts = [set(range(1, self.MAX)) for c in "xmas"]
        print()
        return self._forward_paths_to(start, opts)

    def _forward_paths_to(
        self, source: Name, sets_in: list[set[int]], log_prefix=""
    ) -> int:
        if source == "A":
            ls = [len(s) for s in sets_in]
            amount = reduce(operator.mul, ls, 1)
            # print(f"{log_prefix}ACCEPT {amount} from {ls}")
            return amount
        if source == "R":
            return 0
        flow_name, conds, default = self._flows[source]
        total = 0
        sets = sets_in[:]
        for cond in conds:
            char, op, const, to = cond
            cidx = self.letter_idx[char]
            if op == "<":  # var < const
                op_set = set(range(1, const))
                neg_set = set(range(const, self.MAX))
            else:  # var > const
                op_set = set(range(const + 1, self.MAX))
                neg_set = set(range(1, const + 1))
            new_sets = [
                (s.intersection(op_set) if i == cidx else s) for i, s in enumerate(sets)
            ]
            extra = self._forward_paths_to(to, new_sets, log_prefix+"  ")
            total += extra
            sets = [
                (s.intersection(neg_set) if i == cidx else s)
                for i, s in enumerate(sets)
            ]
        extra = self._forward_paths_to(default, sets, log_prefix+"  ")
        total += extra
        return total


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
    result = computer.forward_paths()
    return result


class Tests(unittest.TestCase):
    def assertNumEqual(self, x, y):
        self.assertEqual(x, y, f"{x} != {y} ({y-x})")

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
        self.assertNumEqual(167409079868000, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(130090458884662, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
