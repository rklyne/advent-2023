from typing import Tuple, NewType, Iterable, Dict, Literal
import typing
import unittest

from data import data, example, example2


Name = NewType("Name", str)
Signal = Literal["low", "high"]
LOW: Signal = "low"
HIGH: Signal = "high"
Op = Literal["%", "&", ""]
NAND: Op = "&"
TOGGLE: Op = "%"
Instr = Tuple[Name, Op, list[Name]]
Input = list[Instr]


def _parse(input: str) -> Iterable[Instr]:
    for line in input.split("\n"):
        name, targets = line.split(" -> ")
        op: Op = ""
        if name[0] in "&%":
            op = name[0]
            name = name[1:]
        yield (Name(name), op, [Name(t) for t in targets.split(", ")])


def parse(i: str) -> Input:
    return list(_parse(i))


def _invert(s: Signal) -> Signal:
    if s == LOW:
        return HIGH
    return LOW


ONE_HIGH = set([HIGH])


class Computer:
    _inputs: Dict[Name, Tuple[Op, list[Name]]]
    _next: Dict[Name, list[Name]]
    _prev: Dict[Name, list[Name]]
    _pending: list[Tuple[Name, Signal, Name]]
    _records: Dict[Name, Tuple[int, int]]

    def __init__(self, inputs: Input):
        self._inputs = {n: (op, ns) for n, op, ns in inputs}
        self._next = {n: ns for n, op, ns in inputs}
        self._prev = {}
        for src, _, ns in inputs:
            for n in ns:
                self._prev.setdefault(n, []).append(src)
        self._pending = []
        self._records = {}
        self._loops = 0
        self._state = {n: self._initial_state(op, n) for n, op, ns in inputs}
        self._send_high = 0
        self._send_low = 0

    def _initial_state(self, op: Op, name: Name):
        if op == TOGGLE:
            return LOW
        if op == NAND:
            return {n: LOW for n in self._prev[name]}

    def _send(self, src: Name, signal: Signal):
        for n in self._next[src]:
            self._send_to(n, signal, src)

    def _send_to(self, target: Name, signal: Signal, src: Name):
        self._pending.append((target, signal, src))
        if signal == HIGH:
            self._send_high += 1
        else:
            self._send_low += 1

    def process_step(self, trigger: Name = Name("broadcaster"), signal: Signal = LOW):
        self._send_to(trigger, signal, "none")
        while self._pending:
            n, s, f = self._pending.pop()
            self._compute(n, s, f)
            self._loops += 1

    def _compute(self, target: Name, signal: Signal, src: Name):
        if target not in self._inputs:
            return
        op, _ = self._inputs[target]
        if op == TOGGLE:
            if signal == LOW:
                self._state[target] = _invert(self._state[target])
                self._send(target, self._state[target])
        elif op == NAND:
            state = self._state[target]
            state[src] = signal
            if set(state.values()) == ONE_HIGH:
                out = LOW
            else:
                out = HIGH
            self._send(target, out)
        elif op == "":
            self._send(target, signal)
        else:
            raise RuntimeError("oops", op)

    def read(self, n: Name) -> Tuple[int, int]:
        return self._send_low, self._send_high
        return self._records.get(n, (0, 0))

    def debug(self):
        return {"loops": self._loops}


def part1(input: Input):
    computer = Computer(input)
    # computer.process_step()
    for i in range(1000):
        computer.process_step()
    low, high = computer.read(Name("output"))
    print(f"loops ({low}, {high}): {computer.debug()}")
    return low * high


def part2(input: Input):
    return 0


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(("broadcaster", "", ["a", "b", "c"]), parse(example)[0])

    def test_part1_example_answer(self):
        self.assertEqual(32000000, part1(parse(example)))

    def test_part1_example2_answer(self):
        self.assertEqual(11687500, part1(parse(example2)))

    def test_part1_answer(self):
        self.assertEqual(806332748, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(-1, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
