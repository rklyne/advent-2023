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
    letter_idx: Dict[Name, int] = {
        "x": 0,
        "m": 1,
        "a": 2,
        "s": 3,
    }

    def __init__(self, flows: list[Flow]):
        self.flows = flows
        self._flows = {
            f[0]: f
            for f in flows
        }
        self._flow_functions = {
            f: self._mk_f(cs, d)
            for (f, cs, d) in flows
        }
        self._reversed_flows = {}
        for (f, cs, d) in flows:
            for c in cs:
                self._reversed_flows.setdefault(c[3], []).append(f)
            self._reversed_flows.setdefault(d, []).append(f)

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

    def process(self, instr: Input) -> int:
        pos = "in"
        while True:
            if pos == "A":
                return sum(instr)
            if pos == "R":
                return 0
            pos = self._flow_functions[pos](instr)
        raise RuntimeError("bad looping")

    def paths_to(self, target, start="in"):
        opts = [
            set(range(1, self.MAX))
            for c in 'xmas'
        ]
        return self._paths_to('A', opts, start)

    def _paths_to(self, target: Name, sets_in: list[set[int]], finish: Name):
        print(f"_paths_to({target}, {[len(s) for s in sets_in]}, {finish})")
        if target == finish:
            return reduce(operator.mul, list(map(len, sets_in)), 1)
        names = self._reversed_flows[target]
        # TODO:
        """
        the plan:
        - for each flow that ends at X:
            - (pre inverted from Y: [X] to X: [Y])
            - for each of the forward conditions from Y:
                - add recursive call to arrives at Y, with set limited by condition
                - update my sets to limit by negated condition
                - add recursion to default by my final sets
        """
        total = 0
        print(f"names[{target}] = {names}")
        for name in names:
            if name == "R":
                continue
            sets = sets_in
            _, conds, default = self._flows[name]
            for char, op, const, to in conds:
                cidx = self.letter_idx[char]
                op_set = set(range(1, const))
                neg_set = set(range(const+1, self.MAX))
                if op == ">":
                    op_set, neg_set = neg_set, op_set
                if to == target:
                    new_sets = [(s.intersection(op_set) if i == cidx else s) for i, s in enumerate(sets)]
                    total += self._paths_to(name, new_sets, finish)
                    break
                sets = [(s.intersection(neg_set) if i == cidx else s) for i, s in enumerate(sets)]
            else:
                if default == target:
                    total += self._paths_to(name, sets, finish)
                else:
                    raise RuntimeError(target, names, name, conds, default)
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
    result = computer.paths_to('A')
    return result


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

    @unittest.skip
    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
